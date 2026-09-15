# 🪚 المقطعُ الجاهز لشاشة الورشة — سحبُ الأصناف والألوان من أودو

**لمن**: الشخصُ اللي يشتغل على شاشة الورشة (كودُها ⛔ مو عندي).
**شنو يسوّي**: يخلّي الشاشةَ تعرض **الحقيقيَّ اللي بالنظام** لحظةَ يفتحها
الزبون — الألوانُ والمقاساتُ والأسعارُ و«متوفّر/نافد» — ومعه بحثٌ بالاسم.
**الأساس**: قرارُ المالك ٠٩-١٥ — «ما يختار اللي موجود افتراضياً، يشوف
الحقيقي اللي عندنا بالنظام ويختار اللون اللي يريده، وحتى يبحث».

---

## ① قبل الكود: خطوتان بأودو (مرّةً وحدة)

1. **علّم الأصنافَ**: المبيعات ← المنتجات ← علّم الأصنافَ اللي تريدها ⇒
   من قائمة الإجراءات «أظهرها بورشة التقطيع» ⇒ اختر الدور (لوحٌ للتقطيع ·
   شريطُ حافة) ومقاسَ اللوح. تشوف المعلَّمَ كلَّه بقائمة **«أصنافُ ورشة
   التقطيع»**.
   ⚠️ اللي ⛔ ما ينعلّم ⛔ ما يظهر بالشاشة — وهذا قصدٌ لا سهو.
2. **المفتاح**: الإعدادات ← المعاملات (`ir.config_parameter`) ←
   `nobel_base.cutting_secret` = نصٌّ طويلٌ عشوائي. هذا مفتاحُ الشاشة.
   ⛔ بلا مفتاحٍ البابُ مقفولٌ تماماً.

---

## ② الرابط

```
GET  https://<عنوان-أودو>/nbl/cutting/catalog
     ?q=<كلمةُ بحث الزبون>          (اختياري)
     &company_id=<رقمُ الدفتر>       (اختياري — الافتراضي دفترُ فرع الورشة)
Authorization: Bearer <المفتاح>
```

المفتاحُ بالترويسة أنظف؛ ويقبلُ كذلك `?key=<المفتاح>` لو الشاشةُ ما
تقدر تبعث ترويسة.

**الجواب** (`application/json`، ترميز UTF-8):

```json
{
  "company":  "شركة نوبل",
  "currency": "IQD",
  "boards": [{
    "odoo_id": 412,
    "name": "لوح MDF ١٨مم أبيض",
    "price": 42000,
    "in_stock": true,
    "sheet_id": 3,  "sheet_label": "١٨مم ١٨٣×٢٤٤",
    "width_cm": 183, "height_cm": 244, "thickness_mm": 18
  }],
  "edges":  [{ "odoo_id": 530, "name": "شريط حافة أبيض ٢٢مم",
               "price": 500, "in_stock": true, "uom": "متر" }],
  "sheets": [{ "id": 3, "label": "١٨مم ١٨٣×٢٤٤", "width_cm": 183,
               "height_cm": 244, "thickness_mm": 18,
               "cut_min": 5, "cut_max": 244, "max_pieces": 40 }],
  "edge_rates": { "retail": 750, "bulk": 500, "bulk_from_m": 50 }
}
```

⛔ **ولا كميةٍ ولا كلفةٍ ولا مورّد** بالحمولة — «متوفّر/نافد» وبس.
والحالاتُ الأخرى: `403` مفتاحٌ غلط أو ناقص · `400` ماكو دفترٌ لفرع الورشة
— والاثنان يرجّعان `{"error": "…"}` بالعربي، اعرضْه كما هو للفنّي.

---

## ③ المقطع (JavaScript — انسخْه كما هو)

```js
const NBL = {
  base: 'https://<عنوان-أودو>',
  key:  '<المفتاح>',          // ⚠️ خلّيه بإعدادات الخادم مال الشاشة
};

// يسحب الكتالوغ. word = كلمةُ بحث الزبون (اختيارية).
async function nblFetchCatalog(word = '') {
  const url = new URL('/nbl/cutting/catalog', NBL.base);
  if (word) url.searchParams.set('q', word);
  const res = await fetch(url, {
    headers: { Authorization: 'Bearer ' + NBL.key },
    cache: 'no-store',
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'تعذّر الاتصالُ بأودو');
  return data;                       // {boards, edges, sheets, edge_rates}
}

// يرسم الألوان. النافدُ يبقى معروضاً ⛔ لكن ما ينضغط.
function nblRenderBoards(boards, container, onPick) {
  container.innerHTML = '';
  if (!boards.length) {
    container.textContent = 'ماكو ألوانٌ مطابقة';
    return;
  }
  for (const board of boards) {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'nbl-board' + (board.in_stock ? '' : ' nbl-out');
    card.disabled = !board.in_stock;
    card.dataset.odooId = board.odoo_id;     // 🔴 ابعثه مع الطلب
    card.innerHTML =
      '<span class="nbl-name">' + board.name + '</span>' +
      '<span class="nbl-size">' + board.width_cm + '×' + board.height_cm +
      ' · ' + board.thickness_mm + 'مم</span>' +
      '<span class="nbl-price">' +
        board.price.toLocaleString('ar-IQ') + ' د.ع</span>' +
      (board.in_stock ? '' : '<span class="nbl-tag">نافد</span>');
    card.onclick = () => onPick(board);
    container.appendChild(card);
  }
}

// البحث: ⛔ ولا نداءَ مع كل حرف — ننتظر ٣٠٠ملي بعد آخر ضغطة.
function nblWireSearch(input, container, onPick) {
  let timer = null;
  const run = async () => {
    try {
      const data = await nblFetchCatalog(input.value.trim());
      nblRenderBoards(data.boards, container, onPick);
    } catch (error) {
      container.textContent = error.message;
    }
  };
  input.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(run, 300);
  });
  run();                                     // أولُ رسمةٍ بلا بحث
}
```

**نقطتان مهمّتان**:

* `odoo_id` هو **مفتاحُ الربط**: ابعثْه مع طلب التقطيع بخانة
  `product_id` من حمولة `nbl_cutting_intake` (ومعه `sheet_id` من نفس
  البطاقة) بدل اسم اللون النصّي — الاسمُ يتغيّر، والرقمُ لا.
* ⛔ **لا تخزّن الجوابَ بالشاشة**: الرصيدُ يتغيّر بالدقيقة، والخادمُ يرجّع
  `Cache-Control: no-store` قصداً. اسحبْ لحظةَ يفتح الزبونُ الصفحة.

---

## ④ المفتاحُ — حيث يُخزَّن

⛔ **لا تكتبه بكود الصفحة** (أي زبونٍ يفتح «مصدر الصفحة» يقراه). خلّيه
بإعدادات **خادم** الشاشة، والصفحةُ تنادي خادمَها وهو ينادي أودو. ولو
الشاشةُ صفحةٌ بلا خادم، خلّها تنادي عبر وسيطٍ بسيطٍ يحمل المفتاح.

---

## ⑤ الباقي على المالك

* **(أ)** كودُ الشاشة بمستودعٍ توصله لي ⇒ أربطُه بنفسي وأقيسُه بالصور؛ أو
* **(ب)** هذا المقطعُ لمن يشتغل على الشاشة — وهو جاهزٌ الآن.
