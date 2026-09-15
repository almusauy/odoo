# -*- coding: utf-8 -*-
# ============================================================================
#  فحص ١ — «شنو عندك من موديولات Enterprise؟»   (nbl_probe_enterprise)
# ============================================================================
#  ⛔ هذا الملف **ما ينصّب ولا يعدّل ولا يحذف أي شي**. قراءةٌ فقط:
#     يقرأ جدول الموديولات (`ir.module.module`) ويطلع تقريراً نصياً.
#
#  🎯 ليش موجود:
#     بيئة التطوير عندي فيها Community فقط (٥٩٦ موديول · صفر Enterprise).
#     فما أعرف — ولا أخمّن — شنو يمنحك اشتراكك فعلاً ولا بأي إصدار.
#     هذا الملف يجيب الجواب **من قاعدتك انته**، لا من ذاكرتي.
#
#  ▶️ شلون تشغّله (الطريق الأسهل — بلا شِل ولا SSH ولا كلمة مرور):
#     ١) على فرع staging: فعّل «وضع المطوّر»
#        الإعدادات ← عام ← أدوات المطوّر ← «تفعيل وضع المطوّر»
#     ٢) التطبيقات ← (قائمة النقاط الثلاث) ← **«تحديث قائمة التطبيقات»**
#        ⚠️ خطوة لازمة: بدونها الجدول قديم وممكن الجواب يطلع ناقصاً.
#     ٣) الإعدادات ← تقني ← الأتمتة ← **إجراءات الخادم** ← جديد
#          الاسم        : NBL Probe 1
#          الموديل      : Company  (`res.company`)
#          نوع الإجراء  : تنفيذ كود بايثون
#          الكود        : الصق **كل** محتوى هذا الملف
#     ٤) احفظ ← زر ⚙️ ← **«تشغيل»**
#     ⇒ ينزّل عندك ملف `nbl_probe_1.txt` — دزّه لي كما هو.
#
#  🔐 ما بالتقرير: أسماء موديولات وحالاتها ورقم إصدار أودو واسم القاعدة.
#     ⛔ ماكو زبائن ولا أسعار ولا أرصدة ولا كلمات مرور — افتح الملف وتأكد
#        بنفسك قبل ما تدزّه.
#
#  📌 قيود التنفيذ (`safe_eval` مال إجراءات الخادم):
#     ماكو `import` ولا `open` ولا `getattr` ولا f-strings — لهذا الكود
#     تحت مكتوب بـ ORM ونسبة `%` فقط. لا تعدّله.
# ============================================================================

L = []

# ---------------------------------------------------------------- ١) الهوية
L.append("=" * 62)
L.append("NBL PROBE 1 - Enterprise availability")
L.append("=" * 62)
L.append("db            : %s" % env.cr.dbname)
L.append("odoo version  : %s" % (env['ir.module.module'].search(
    [('name', '=', 'base')], limit=1).latest_version or '?'))
L.append("companies     : %s" % env['res.company'].sudo().search_count([]))
L.append("modules total : %s" % env['ir.module.module'].sudo().search_count([]))
L.append("")

# ------------------------------------------------ ٢) هل النسخة Enterprise؟
# الدليل القاطع: موديولات مرخّصة OEEL-1 موجودة بالمسار.
oeel = env['ir.module.module'].sudo().search_count([('license', '=', 'OEEL-1')])
L.append("modules licensed OEEL-1 (= Enterprise on path) : %s" % oeel)
if oeel == 0:
    L.append("  >>> NO Enterprise modules on this instance's addons path.")
L.append("")

# ---------------------------------- ٣) الموديولات اللي تخصّ متطلباتنا فقط
# ⚠️ الأسماء التقنية أدناه **مُثبَتة** من مصدر أودو ١٩ المجتمعي الموجود
#    عندي — لا من الذاكرة:
#      `addons/*/models/res_config_settings.py`  حقول `module_<name>`
#      `addons/base_install_request/__init__.py` قائمة Enterprise صراحةً
#    وأي اسم ما لكيته بدليل تركته برّه هذه القائمة قصداً.
TARGETS = [
    # -- المحاسبة --------------------------------------------------------
    'account_accountant',        # المحاسبة الكاملة (تسويات · إقفال فترات)
    'account_reports',           # الميزانية · الأرباح والخسائر · أعمار الذمم
    'account_budget',            # الموازنات
    'account_3way_match',        # مطابقة ثلاثية: أمر شراء / استلام / فاتورة
    'account_batch_payment',     # دفعات مجمّعة
    'account_iso20022',          # ملفات تحويل بنكية
    'account_inter_company_rules',   # معاملات بين الشركات
    'currency_rate_live',        # سحب أسعار الصرف تلقائياً (يخصّ شغل الصرف)
    # -- الرواتب ---------------------------------------------------------
    'hr_payroll',
    'hr_payroll_account',
    'hr_payroll_expense',
    'hr_contract',
    # -- مبيعات ومخزن ----------------------------------------------------
    'sale_commission',           # سلّم العمولات المتدرّج
    'stock_barcode',             # الباركود بالمخزن
    'quality_control',           # فحص الجودة عند الاستلام (درجات الخشب)
    'mrp_mps',
    # -- مستندات وتوقيع --------------------------------------------------
    'documents',
    'documents_account',
    'documents_hr',
    'sign',
    'approvals',
    'knowledge',
    # -- أخرى ذُكرت بالنقاش ----------------------------------------------
    'planning',
    'appointment',
    'helpdesk',
    'hr_appraisal',
    'hr_recruitment',
    'voip',
    'web_studio',
    'spreadsheet_dashboard',
    # -- Community لازم ننصّبه (للمقارنة بنفس التقرير) --------------------
    'crm',
    'project',
    'maintenance',
]

rows = env['ir.module.module'].sudo().search_read(
    [('name', 'in', TARGETS)],
    ['name', 'shortdesc', 'state', 'license', 'latest_version', 'application'])

found = {}
for r in rows:
    found[r['name']] = r

L.append("-" * 62)
L.append("%-26s %-12s %-9s %s" % ('MODULE', 'STATE', 'LICENSE', 'VERSION'))
L.append("-" * 62)
for name in TARGETS:
    r = found.get(name)
    if not r:
        L.append("%-26s %-12s %-9s %s" % (name, 'ABSENT', '-', '-'))
    else:
        L.append("%-26s %-12s %-9s %s" % (
            name,
            r['state'] or '?',
            r['license'] or '?',
            r['latest_version'] or '-'))
L.append("-" * 62)
L.append("")

# --------------- ٤) أي موديولات عراقية موجودة (للرواتب والمحاسبة معاً)
l10n = env['ir.module.module'].sudo().search_read(
    [('name', 'like', 'l10n_iq')],
    ['name', 'state', 'license'])
L.append("Iraqi localization modules on path:")
if not l10n:
    L.append("  (none)")
for r in l10n:
    L.append("  %-24s %-12s %s" % (r['name'], r['state'], r['license'] or '?'))
L.append("")

# --- ٥) هل أكو قواعد رواتب جاهزة لأي بلد؟ (يبيّن هل الرواتب تحتاج بناءً)
pay = env['ir.module.module'].sudo().search_read(
    [('name', 'like', 'payroll'), ('state', '=', 'installed')],
    ['name', 'state'])
L.append("payroll-related modules already INSTALLED: %s" % len(pay))
for r in pay:
    L.append("  %s" % r['name'])
L.append("")

# ------------------------------------- ٦) المنصَّب حالياً كله (اسم فقط)
inst = env['ir.module.module'].sudo().search_read(
    [('state', '=', 'installed')], ['name'], order='name')
L.append("INSTALLED MODULES (%s):" % len(inst))
L.append(", ".join([r['name'] for r in inst]))
L.append("")
L.append("== END NBL PROBE 1 ==")

TXT = "\n".join(L)

# ---------------------------------------------------------- إخراج التقرير
# الافتراضي: ملف ينزل عندك (يتحمّل أي طول).
att = env['ir.attachment'].create({
    'name': 'nbl_probe_1.txt',
    'type': 'binary',
    'mimetype': 'text/plain',
    'datas': b64encode(TXT.encode('utf-8')),
})
action = {
    'type': 'ir.actions.act_url',
    'url': '/web/content/%s?download=1' % att.id,
    'target': 'self',
}

# 🔁 إذا ما نزل الملف لأي سبب: احذف السطور الأربعة اللي فوق (`action = {...}`)
#    وشيل علامة التعليق عن السطر التالي — راح يطلع التقرير بنافذة تنسخ منها:
# raise UserError(TXT)
