import os
WORK = os.environ.get('NBL_MANUAL_WORK', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work'))
CHROME = os.environ.get('NBL_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
import sys, os, json, time
from playwright.sync_api import sync_playwright
BASE = 'http://127.0.0.1:9096'
ROOT = WORK + '/manual/flows'
os.makedirs(ROOT, exist_ok=True)
A = lambda x: '/odoo/action-' + x
FLOWS = {
 'fixup3': [
  ('k_bundle', A('nobel_base.action_nbl_bundle_break'), []),
 ],
 'fixup2': [
  ('k_delivery_return', A('stock.action_picking_tree_all') + '/217', [('click', 'button:has-text("مرتجع")'), ('wait', 4000)]),
  ('k_delivery_done', A('stock.action_picking_tree_all') + '/217', []),
 ],
 'fixup': [
  ('s_suggest_karrada', A('sale.action_orders') + '/129', [('click', 'button:has-text("اقتراحات ذكية")'), ('wait', 4000)]),
  ('s_unified_own', A('nobel_base.action_nbl_order') + '/47', []),
  ('s_receipt_cash_own', A('nobel_base.action_nbl_payment') + '/7', []),
  ('s_receipt_sk_draft', A('nobel_base.action_nbl_payment') + '/63', []),
 ],
 'none': [
  ('login', '/web/login', []),
 ],
 'qusai': [
  ('s_dash', A('nobel_base.action_nbl_dashboard'), []),
  ('s_quotes_list', A('sale.action_quotations_with_onboarding'), []),
  ('s_quote_new', A('sale.action_quotations_with_onboarding') + '/new', []),
  ('s_quote_ok', A('sale.action_orders') + '/125', []),
  ('s_suggest', A('sale.action_orders') + '/125', [('click', 'button:has-text("اقتراحات ذكية")'), ('wait', 4000)]),
  ('s_quote_low_block', A('sale.action_orders') + '/126', [('click', 'button:has-text("تأكيد")'), ('wait', 4000)]),
  ('s_order_confirmed', A('sale.action_orders') + '/123', []),
  ('s_unified_list', A('nobel_base.action_nbl_order'), []),
  ('s_unified_form', A('nobel_base.action_nbl_order') + '/112', []),
  ('s_unified_new', A('nobel_base.action_nbl_order') + '/new', []),
  ('s_invoices_list', A('account.action_move_out_invoice_type'), []),
  ('s_invoice', A('account.action_move_out_invoice_type') + '/464', []),
  ('s_invoice_return', A('account.action_move_out_invoice_type') + '/464', [('click', 'button:has-text("مرتجع")'), ('wait', 4000)]),
  ('s_receipt_list', A('nobel_base.action_nbl_payment'), []),
  ('s_receipt_new', A('nobel_base.action_nbl_payment') + '/new', []),
  ('s_receipt_cash', A('nobel_base.action_nbl_payment') + '/48', []),
  ('s_receipt_superkey', A('nobel_base.action_nbl_payment') + '/49', []),
  ('s_statement', A('nobel_base.action_nbl_customer_statement'), []),
  ('s_partner_summary', A('nobel_base.action_nbl_partner_summary'), []),
  ('s_cashbox', A('nobel_base.action_nbl_branch_cashbox'), []),
  ('s_credit_req', A('nobel_base.action_nbl_credit_request') + '/1', []),
  ('s_reset_req', A('nobel_base.action_nbl_move_reset') + '/2', []),
  ('s_supply', A('nobel_base.action_nbl_supply_request_mine') + '/38', []),
  ('s_cutting', A('nobel_base.action_nbl_cutting_order'), []),
  ('s_cutting_form', A('nobel_base.action_nbl_cutting_order') + '/12', []),
  ('s_referral', A('nobel_base.action_nbl_referral'), []),
  ('s_loyalty', A('nobel_base.action_nbl_loyalty_award'), []),
  ('s_an_sales', A('nobel_base.action_nbl_an_sales'), [('wait', 4000)]),
  ('s_customers', '/odoo/contacts', []),
  ('s_face', A('nobel_base.action_nbl_face_punch'), [('wait', 3000)]),
  ('s_expense_my', A('hr_expense.hr_expense_actions_my_all'), []),
  ('s_activities', A('mail.mail_activity_action'), []),
 ],
 'ali.m': [
  ('k_overview', A('stock.stock_picking_type_action'), []),
  ('k_receipts', A('stock.action_picking_tree_incoming'), []),
  ('k_receipt_form', A('stock.action_picking_tree_all') + '/207', []),
  ('k_deliveries', A('stock.action_picking_tree_outgoing'), []),
  ('k_delivery_todo', A('stock.action_picking_tree_all') + '/218', []),
  ('k_delivery_done', A('stock.action_picking_tree_all') + '/217', []),
  ('k_delivery_return', A('stock.action_picking_tree_all') + '/217', [('click', 'button:has-text("مرتجع")'), ('wait', 4000)]),
  ('k_quants', A('stock.dashboard_open_quants'), []),
  ('k_inventory', A('stock.action_view_inventory_tree'), []),
  ('k_count_queue', A('nobel_base.action_nbl_inventory_count'), []),
  ('k_grade', A('nobel_base.action_nbl_grade_sort'), []),
  ('k_bundle', A('nobel_base.action_nbl_bundle_break') + '/12', []),
  ('k_supply_mine', A('nobel_base.action_nbl_supply_request_mine'), []),
  ('k_stock_an', A('nobel_base.action_nbl_an_stock'), [('wait', 4000)]),
 ],
 'm.i12345': [
  ('a_dash', A('account.open_account_journal_dashboard_kanban'), []),
  ('a_invoices', A('account.action_move_out_invoice_type'), []),
  ('a_invoice', A('account.action_move_out_invoice_type') + '/464', []),
  ('a_bills', A('account.action_move_in_invoice_type'), []),
  ('a_bill', A('account.action_move_in_invoice_type') + '/411', []),
  ('a_payments', A('account.action_account_payments'), []),
  ('a_receipts', A('nobel_base.action_nbl_payment'), []),
  ('a_sk_settle', A('nobel_base.action_nbl_superkey_settle'), []),
  ('a_sk_pool', A('nobel_base.action_nbl_superkey_pool'), []),
  ('a_cash_deposit', A('nobel_base.action_nbl_cash_deposit') + '/1', []),
  ('a_cash_count', A('nobel_base.action_nbl_cash_count'), []),
  ('a_audit_queue', A('nobel_base.action_nbl_audit_queue'), []),
  ('a_statement', A('nobel_base.action_nbl_customer_statement'), []),
  ('a_supplier_stmt', A('nobel_base.action_nbl_supplier_statement'), []),
  ('a_collection_days', A('nobel_base.action_nbl_collection_days'), []),
  ('a_move_reset', A('nobel_base.action_nbl_move_reset'), []),
  ('a_date_grant', A('nobel_base.action_nbl_date_grant'), []),
  ('a_expenses', A('hr_expense.hr_expense_actions_all'), []),
  ('a_expense', A('hr_expense.hr_expense_actions_all') + '/17', []),
  ('a_report_ar', A('account_reports.action_account_report_ar'), [('wait', 5000)]),
  ('a_report_bs', A('account_reports.action_account_report_bs'), [('wait', 5000)]),
  ('a_an_finance', A('nobel_base.action_nbl_an_finance'), [('wait', 4000)]),
  ('a_followup', A('nobel_base.action_nbl_followup_mine'), []),
 ],
 'fadil': [
  ('g_activities', A('mail.mail_activity_action') + '?cids=2-3-4', []),
  ('g_po_pending', A('purchase.purchase_rfq') + '/66?cids=2-3-4', []),
  ('g_sk_waiting', A('nobel_base.action_nbl_superkey_waiting') + '?cids=2-3-4', []),
  ('g_credit_reqs', A('nobel_base.action_nbl_credit_request') + '?cids=2-3-4', []),
  ('g_credit_req', A('nobel_base.action_nbl_credit_request') + '/1?cids=2-3-4', []),
  ('g_move_reset', A('nobel_base.action_nbl_move_reset') + '/2?cids=2-3-4', []),
  ('g_count_queue', A('nobel_base.action_nbl_inventory_count') + '?cids=2-3-4', []),
  ('g_supply', A('nobel_base.action_nbl_supply_request') + '?cids=2-3-4', []),
  ('g_supply_form', A('nobel_base.action_nbl_supply_request') + '/38?cids=2-3-4', []),
  ('g_roles', A('nobel_base.action_nbl_role') + '?cids=2-3-4', []),
  ('g_role_form', A('nobel_base.action_nbl_role') + '/4?cids=2-3-4', []),
  ('g_role_grants', A('nobel_base.action_nbl_role_grant') + '?cids=2-3-4', []),
  ('g_users', A('base.action_res_users') + '?cids=2-3-4', []),
  ('g_user_qusai', A('base.action_res_users') + '/%s?cids=2-3-4' % 'QUSAI_ID', []),
  ('g_pricing_grid', A('nobel_base.action_nbl_pricing_grid') + '?cids=2-3-4', [('wait', 3000)]),
  ('g_pricing_board', A('nobel_base.action_nbl_pricing_board') + '?cids=2-3-4', []),
  ('g_price_sugg', A('nobel_base.action_nbl_price_suggestions') + '?cids=2-3-4', []),
  ('g_fx_entry', A('nobel_base.action_nbl_currency_rate_entry') + '?cids=2-3-4', []),
  ('g_fx_history', A('nobel_base.action_nbl_currency_rate_history') + '?cids=2-3-4', []),
  ('g_company', A('base.action_res_company_form') + '/2?cids=2-3-4', []),
  ('g_digest', A('nobel_base.action_nbl_digest') + '?cids=2-3-4', []),
  ('g_an_owner', A('nobel_base.action_nbl_an_owner') + '?cids=2-3-4', [('wait', 5000)]),
  ('g_sales_dash', A('nobel_base.action_nbl_sales_dash') + '?cids=2-3-4', [('wait', 5000)]),
  ('g_po_list', A('purchase.purchase_rfq') + '?cids=2-3-4', []),
  ('g_po_import', A('purchase.purchase_rfq') + '/55?cids=2-3-4', []),
  ('g_container', A('purchase.purchase_rfq') + '/55?cids=2-3-4', [('click', 'button:has-text("وصلني من الحاوية")'), ('wait', 4000)]),
  ('g_vendor_perf', A('nobel_base.action_nbl_vendor_perf') + '?cids=2-3-4', []),
  ('g_bills_audit', A('nobel_base.action_nbl_audit_queue') + '?cids=2-3-4', []),
  ('g_employees', A('hr.open_view_employee_list_my') + '?cids=2-3-4', []),
  ('g_attendance', A('hr_attendance.hr_attendance_action') + '?cids=2-3-4', []),
  ('g_penalty', A('nobel_base.action_nbl_attendance_penalty') + '?cids=2-3-4', []),
  ('g_payslips', A('hr_payroll.action_view_hr_payslip_month_form') + '?cids=2-3-4', []),
  ('g_leaves', A('hr_holidays.hr_leave_action_action_approve_department') + '?cids=2-3-4', []),
  ('g_bio', A('nobel_base.action_nbl_bio_device') + '?cids=2-3-4', []),
  ('g_login_blocks', A('nobel_base.action_nbl_login_block') + '?cids=2-3-4', []),
  ('g_role_changes', A('nobel_base.action_nbl_role_change') + '?cids=2-3-4', []),
  ('g_tax_assess', A('nobel_base.action_nbl_tax_assessment') + '?cids=2-3-4', []),
  ('g_income_tax', A('nobel_base.action_nbl_income_tax') + '?cids=2-3-4', []),
  ('g_breakeven', A('nobel_base.action_nbl_breakeven') + '?cids=2-3-4', []),
 ],
 'm.hasan': [
  ('c_cashbox', A('nobel_base.action_nbl_branch_cashbox'), []),
  ('c_cash_count_new', A('nobel_base.action_nbl_cash_count') + '/new', []),
  ('c_cash_deposit', A('nobel_base.action_nbl_cash_deposit') + '/1', []),
  ('c_receipt_new', A('nobel_base.action_nbl_payment') + '/new', []),
  ('c_invoices', A('account.action_move_out_invoice_type'), []),
  ('c_statement', A('nobel_base.action_nbl_customer_statement'), []),
  ('c_expense_new', A('hr_expense.hr_expense_actions_my_all') + '/new', []),
 ],
 'ayman': [
  ('r_delivery', A('stock.action_picking_tree_all') + '/145', []),
  ('r_deliveries', A('stock.action_picking_tree_outgoing'), []),
  ('r_orders', A('sale.action_orders'), []),
  ('r_receipt_new', A('nobel_base.action_nbl_payment') + '/new', []),
 ],
}
def login(p, user):
    p.goto(BASE + '/web/login', wait_until='domcontentloaded'); p.wait_for_timeout(1500)
    p.fill('input[name="login"]', user); p.fill('input[name="password"]', 'nobel-test-1234')
    p.click('button[type="submit"]'); p.wait_for_timeout(7000)
    assert '/web/login' not in p.url, 'LOGIN_FAILED ' + user
def run(p, who, items, qusai_id):
    log = []
    for key, url, steps in items:
        url = url.replace('QUSAI_ID', str(qusai_id))
        try:
            p.goto(BASE + url, wait_until='domcontentloaded'); p.wait_for_timeout(6500)
            for st in steps:
                if st[0] == 'click': p.locator(st[1]).first.click(); 
                elif st[0] == 'wait': p.wait_for_timeout(st[1])
                elif st[0] == 'esc': p.keyboard.press('Escape')
                p.wait_for_timeout(800)
            p.screenshot(path=f'{ROOT}/{who}__{key}.png')
            log.append((key, 'ok', p.url))
        except Exception as e:
            try: p.screenshot(path=f'{ROOT}/{who}__{key}.png')
            except Exception: pass
            log.append((key, 'ERR', str(e)[:120]))
        print(who, key, log[-1][1], flush=True)
    return log
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'])
    users = sys.argv[1:] or list(FLOWS)
    qusai_id = int(os.environ.get('QUSAI_ID', '0'))
    for who in users:
        ctx = b.new_context(viewport={'width': 1500, 'height': 1000}, permissions=['camera']); p = ctx.new_page()
        if who == 'fixup3':
            login(p, 'ali.m'); run(p, 'ali.m', FLOWS['fixup3'], qusai_id); ctx.close(); continue
        if who == 'fixup2':
            login(p, 'ali.m'); run(p, 'ali.m', FLOWS['fixup2'], qusai_id); ctx.close(); continue
        if who == 'fixup':
            login(p, 'qusai'); run(p, 'qusai', FLOWS['fixup'], qusai_id); ctx.close(); continue
        if who == 'none':
            p.goto(BASE + '/web/login', wait_until='domcontentloaded'); p.wait_for_timeout(2500); p.screenshot(path=f'{ROOT}/none__login.png'); ctx.close(); continue
        try: login(p, who)
        except Exception as e: print('LOGIN FAIL', who, e); ctx.close(); continue
        run(p, who, FLOWS[who], qusai_id)
        ctx.close()
    b.close()
