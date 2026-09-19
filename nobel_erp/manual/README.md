# 📘 دليل المستخدم المصوَّر — الإصدار ١ (٢٠٢٦-٠٩-١٩)

طلب المالك: «ملف أشاركه مع مستخدمي النظام: كل مستخدم أدواره، شنو عنده أكسس، وورك فلو كامل بالصور».

- `nobel_user_manual_v1_2026-09-19.pdf` — ١١٣ صفحة، ٩ فصول (مشترك · خريطة الأدوار · البائع · أمين المخزن · المندوب · محاسب الفرع · مدير الحسابات · المدير العام · ملاحق).
- `nobel_user_manual_v1_2026-09-19.html` — نفس الدليل بصيغة صفحة (الصور مضمَّنة).
- الأدوات: `crawl_access.py` (يدخل بكل دور ويصوّر تطبيقاته وقوائمه)، `flow_shots.py` (شاشات الورك فلو لكل دور)، `build_manual.py` (يبني HTML من الصور والنص)، `render_pdf.py` (Chromium ⇒ PDF). تشتغل على قاعدة محاكاة (`http://127.0.0.1:9096`) بكلمة السر التجريبية `nobel-test-1234`.

مجلد الشغل يُضبط بمتغيّر البيئة `NBL_MANUAL_WORK` (الافتراضي `./work` بجانب السكربتات)، ومسار كروم بـ`NBL_CHROME`. الصور تُكتب تحت `work/manual/` وصور «متابعتي اليوم» والإشعارات تحت `work/fu/` و`work/notif/`.

لتحديث الدليل بعد تغيير بالنظام:

```
python crawl_access.py qusai ali.m m.i12345 fadil ali.s m.hasan ayman mustaf
QUSAI_ID=<id> python flow_shots.py none qusai ali.m m.i12345 fadil m.hasan ayman
python build_manual.py            # ⇒ work/manual/nobel_user_manual.html
python render_pdf.py work/manual/nobel_user_manual.html work/manual/nobel_user_manual.pdf
```

ثم انسخ الملفين باسم مؤرَّخ جديد بجانب هذا الملف.
