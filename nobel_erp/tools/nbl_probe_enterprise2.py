# -*- coding: utf-8 -*-
# ============================================================================
#  فحص ٢ — «شنو داخل الموديولات اللي نصّبتها؟»  (nbl_probe_enterprise2)
# ============================================================================
#  ⛔ قراءةٌ فقط — ما ينصّب ولا يعدّل ولا يحذف.
#
#  🎯 ليش موجود:
#     بعد ما تنصّب موجةً من موديولات Enterprise، أحتاج **الأسماء
#     الحقيقية** للموديلات والحقول اللي جابتها — لأن كتابة كود ربطٍ
#     يستدعي حقلاً ما شفته = اختراع، وقاعدتنا «لا تخترع».
#     هذا الملف يجيبها من قاعدتك، فأكتب الجسر على دليلٍ لا على ظن.
#
#  ▶️ نفس طريقة الفحص الأول:
#     الإعدادات ← تقني ← الأتمتة ← إجراءات الخادم ← جديد
#        الاسم       : NBL Probe 2
#        الموديل     : Company  (`res.company`)
#        نوع الإجراء : تنفيذ كود بايثون
#        الكود       : الصق كل محتوى هذا الملف
#     احفظ ← ⚙️ ← تشغيل  ⇒  ينزل `nbl_probe_2.txt` — دزّه لي.
#
#  ✏️ **الشي الوحيد اللي تعدّله**: سطر `MODULES` تحت — حطّ بيه أسماء
#     اللي نصّبته فعلاً. إذا خلّيته فاضياً، ياخذ **كل** موديول
#     مرخَّص `OEEL-1` ومنصَّب عندك (وهذا الغالب أسهل).
#
#  🔐 ما بالتقرير: أسماء موديلات وحقول ومجموعات صلاحيات — **بنيةٌ لا
#     بيانات**. ⛔ ماكو زبائن ولا أسعار ولا أرصدة ولا كلمات مرور.
# ============================================================================

# ✏️ عدّل هنا فقط (مثال: ['account_accountant', 'account_reports'])
MODULES = []

L = []
L.append("=" * 62)
L.append("NBL PROBE 2 - installed module internals")
L.append("=" * 62)
L.append("db : %s" % env.cr.dbname)

Mod = env['ir.module.module'].sudo()
Data = env['ir.model.data'].sudo()

# ── تحديد الموديولات المقصودة ───────────────────────────────────────
if MODULES:
    mods = Mod.search_read(
        [('name', 'in', MODULES)], ['name', 'state', 'license'])
else:
    mods = Mod.search_read(
        [('license', '=', 'OEEL-1'), ('state', '=', 'installed')],
        ['name', 'state', 'license'], order='name')

L.append("modules probed : %s" % len(mods))
L.append("")
for m in mods:
    L.append("  %-32s %-12s %s" % (m['name'], m['state'], m['license'] or '?'))
L.append("")

names = [m['name'] for m in mods]
if not names:
    L.append(">>> ولا موديول مطابق. إذا نصّبت شيئاً، حطّ اسمه بـMODULES.")

for name in names:
    L.append("")
    L.append("#" * 62)
    L.append("# MODULE: %s" % name)
    L.append("#" * 62)

    # ① الموديلات اللي **يعرّفها** الموديول
    rows = Data.search_read(
        [('module', '=', name), ('model', '=', 'ir.model')],
        ['res_id'], limit=400)
    model_ids = [r['res_id'] for r in rows]
    models_ = env['ir.model'].sudo().search_read(
        [('id', 'in', model_ids)], ['model', 'name'], order='model')
    L.append("")
    L.append("-- MODELS DEFINED (%s) --" % len(models_))
    for mm in models_:
        L.append("  %-42s %s" % (mm['model'], mm['name'] or ''))

    # ② الحقول اللي **يضيفها** الموديول (على موديلاته أو على غيرها)
    rows = Data.search_read(
        [('module', '=', name), ('model', '=', 'ir.model.fields')],
        ['res_id'], limit=3000)
    fids = [r['res_id'] for r in rows]
    flds = env['ir.model.fields'].sudo().search_read(
        [('id', 'in', fids)],
        ['model', 'name', 'ttype', 'relation', 'required', 'store',
         'field_description'],
        order='model,name')
    L.append("")
    L.append("-- FIELDS ADDED (%s) --" % len(flds))
    current = ''
    for f in flds:
        if f['model'] != current:
            current = f['model']
            L.append("  [%s]" % current)
        rel = (' -> ' + f['relation']) if f['relation'] else ''
        flags = []
        if f['required']:
            flags.append('required')
        if not f['store']:
            flags.append('computed/not-stored')
        L.append("      %-34s %-12s%s %s" % (
            f['name'], f['ttype'] or '?', rel,
            ('(' + ', '.join(flags) + ')') if flags else ''))

    # ③ مجموعات الصلاحيات اللي يجيبها — تخصّ ربط أدوارنا
    rows = Data.search_read(
        [('module', '=', name), ('model', '=', 'res.groups')],
        ['res_id', 'name'], limit=300)
    gids = [r['res_id'] for r in rows]
    grps = env['res.groups'].sudo().search_read(
        [('id', 'in', gids)], ['name'], order='name')
    L.append("")
    L.append("-- SECURITY GROUPS (%s) --" % len(grps))
    for r in rows:
        L.append("  %s.%s" % (name, r['name']))

    # ④ اليوميات/الحسابات المحاسبية اللي يضيفها (لو موديول محاسبة)
    rows = Data.search_read(
        [('module', '=', name), ('model', 'in',
                                 ['account.report', 'account.journal'])],
        ['res_id', 'model', 'name'], limit=300)
    L.append("")
    L.append("-- ACCOUNT REPORTS / JOURNALS (%s) --" % len(rows))
    for r in rows:
        L.append("  %-24s %s.%s" % (r['model'], name, r['name']))

L.append("")
L.append("== END NBL PROBE 2 ==")

TXT = "\n".join(L)

att = env['ir.attachment'].create({
    'name': 'nbl_probe_2.txt',
    'type': 'binary',
    'mimetype': 'text/plain',
    'datas': b64encode(TXT.encode('utf-8')),
})
action = {
    'type': 'ir.actions.act_url',
    'url': '/web/content/%s?download=1' % att.id,
    'target': 'self',
}
# 🔁 إذا ما نزل الملف: احذف `action = {...}` وشيل التعليق عن السطر التالي:
# raise UserError(TXT)
