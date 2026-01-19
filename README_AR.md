<div align="center" dir="rtl">

# 🎬 محمّل الكارتون العربي

<img src="docs/images/home.png" width="600" alt="محمّل الكارتون العربي" />

### ⚡ أسرع أداة لتحميل الكارتون العربي

[![الإصدار](https://img.shields.io/badge/الإصدار-4.2.0-00d4ff?style=for-the-badge&labelColor=1a1a2e)](https://github.com/3bkader-gpt/cartoon)
[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb?style=for-the-badge&logo=react&logoColor=white&labelColor=1a1a2e)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=1a1a2e)](https://fastapi.tiangolo.com)
[![الرخصة](https://img.shields.io/badge/الرخصة-MIT-f7df1e?style=for-the-badge&labelColor=1a1a2e)](LICENSE)

<br/>

[✨ المميزات](#-المميزات) •
[🚀 البدء السريع](#-البدء-السريع) •
[📸 صور التطبيق](#-صور-التطبيق) •
[🏗️ البنية التقنية](#️-البنية-التقنية) •
[📖 التوثيق](#-التوثيق)

---

**حمّل مسلسلات كاملة بضغطة واحدة**  
**تخزين مؤقت ذكي • مكتبة شخصية • تصدير جاهز لـ Plex**

</div>

---

<div dir="rtl">

## ✨ المميزات

<table>
<tr>
<td width="50%">

### 🚀 القوة الأساسية
```
✅ جلب حلقات متعددة دفعة واحدة
✅ استخراج البيانات بالتوازي
✅ تخزين SQLite ذكي (24 ساعة)
✅ تصدير لـ IDM و Aria2
✅ روابط تحميل مباشرة
```

</td>
<td width="50%">

### ❤️ إدارة المكتبة
```
✅ نظام المفضلة
✅ وصول سريع للمسلسلات
✅ مزامنة تلقائية للبيانات
✅ معاينة الصور المصغرة
✅ تتبع عدد الحلقات
```

</td>
</tr>
<tr>
<td width="50%">

### ⚙️ التخصيص
```
✅ الوضع الداكن / الفاتح
✅ تسمية ملفات Plex/Kodi
✅ فتح مجلد التحميلات بسرعة
✅ الترتيب والفلترة
✅ تحديد الكل / إلغاء التحديد
```

</td>
<td width="50%">

### 🎯 جودة الاستخدام
```
✅ مؤشر تقدم فوري
✅ مؤشرات الكاش
✅ إعادة تحميل إجبارية
✅ البحث في الحلقات
✅ نسخ الروابط فردياً
```

</td>
</tr>
</table>

---

## 📸 صور التطبيق

<div align="center">

| الرئيسية | المكتبة | الإعدادات |
|:---:|:---:|:---:|
| ![الرئيسية](docs/images/home.png) | ![المكتبة](docs/images/library.png) | ![الإعدادات](docs/images/settings.png) |
| *واجهة التحميل الرئيسية* | *مسلسلاتك المفضلة* | *خصص تجربتك* |

</div>

---

## 🚀 البدء السريع

### المتطلبات

```bash
# مطلوب
Python 3.12+
Node.js 18+
Git
```

### التثبيت

```bash
# 1️⃣ استنساخ المشروع
git clone https://github.com/3bkader-gpt/cartoon.git
cd cartoon

# 2️⃣ تثبيت مكتبات Python
pip install -r requirements.txt
playwright install chromium

# 3️⃣ تثبيت مكتبات الواجهة
cd frontend
npm install
cd ..
```

### التشغيل

<table>
<tr>
<td>

**🖥️ Terminal 1 - الخادم**
```bash
python backend/main.py
```

</td>
<td>

**🌐 Terminal 2 - الواجهة**
```bash
cd frontend
npm run dev
```

</td>
</tr>
</table>

<div align="center">

### 🎉 افتح [http://localhost:5173](http://localhost:5173) وابدأ التحميل!

</div>

---

## 🏗️ البنية التقنية

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      🌐 الواجهة الأمامية (React + Vite)                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐   │
│  │  📥 المحمّل   │    │  ❤️ المكتبة   │    │      ⚙️ الإعدادات         │   │
│  └───────┬──────┘    └───────┬──────┘    └────────────┬─────────────┘   │
│          └───────────────────┼────────────────────────┘                 │
│                              │ طلبات API                                │
└──────────────────────────────┼──────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   ⚡ الخادم الخلفي (FastAPI + Python)                   │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                    🗄️ قاعدة بيانات SQLite                       │     │
│  │  ┌─────────────┐      ┌─────────────┐      ┌─────────────────┐ │     │
│  │  │  المسلسلات  │──────│  الحلقات   │      │    المفضلة      │ │     │
│  │  │ is_favorite │      │ UNIQUE key  │      │    (قديم)       │ │     │
│  │  └─────────────┘      └─────────────┘      └─────────────────┘ │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────────────────┐   │
│  │ 🔍 الكاشط   │  │ 🎭 Playwright │  │      📡 نقاط النهاية API       │   │
│  │   Engine   │──│   Browser   │  │  /season/stream  /library/    │   │
│  └─────────────┘  └─────────────┘  │  /open-downloads /health      │   │
│                                    └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📡 مرجع الـ API

| الطريقة | النقطة | الوصف |
|:------:|--------|-------|
| `GET` | `/api/season/stream` | 📺 بث بيانات الحلقات |
| `GET` | `/api/library/` | ❤️ جلب المفضلة |
| `POST` | `/api/library/toggle` | 🔄 تبديل المفضلة |
| `GET` | `/api/library/check` | ✅ فحص إذا مفضل |
| `GET` | `/api/search` | 🔍 البحث |
| `POST` | `/api/open-downloads` | 📁 فتح مجلد التحميلات |
| `GET` | `/api/health` | 💚 فحص الصحة |

---

## 🗂️ هيكل المشروع

```
cartoon/
├── 🐍 backend/
│   ├── api/
│   │   ├── main_router.py      # API الرئيسي
│   │   └── library_router.py   # API المفضلة
│   ├── scraper/
│   │   └── scraper.py          # الكاشط
│   ├── database.py             # عمليات SQLite
│   └── main.py                 # نقطة البداية
│
├── ⚛️ frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── api.js
│   └── package.json
│
├── 📚 docs/
│   ├── images/
│   ├── PROJECT_STATUS.md
│   └── ROADMAP.md
│
├── 📄 README.md
├── 📄 README_AR.md
└── 📄 LICENSE
```

---

## 🗺️ خريطة الطريق

<div align="center">

| الإصدار | الميزة | الحالة |
|:-------:|--------|:------:|
| v3.0 | المحمّل الأساسي + IndexedDB | ✅ |
| v4.0 | الترحيل لـ SQLite | ✅ |
| v4.1 | ميزة مكتبتي | ✅ |
| v4.2 | الإعدادات + تسمية Plex | ✅ |
| **v5.0** | **مدير التحميلات الداخلي** | 🔜 |
| v6.0 | دعم مصادر متعددة | 📋 |

</div>

---

## 🤝 المساهمة

المساهمات مرحب بها! لا تتردد في إرسال Pull Request.

1. اعمل Fork للمشروع
2. أنشئ فرع الميزة (`git checkout -b feature/ميزة-رائعة`)
3. احفظ التغييرات (`git commit -m 'إضافة ميزة رائعة'`)
4. ادفع للفرع (`git push origin feature/ميزة-رائعة`)
5. افتح Pull Request

---

## 📄 الرخصة

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

<div align="center">

### ⭐ اعمل Star للمشروع إذا أعجبك!

<br/>

---

### 👨‍💻 المطوّر

<a href="https://github.com/3bkader-gpt">
  <img src="https://img.shields.io/badge/محمد%20عمر-مطوّر-blueviolet?style=for-the-badge&logo=github&logoColor=white" alt="Mohamed Omar" />
</a>

<br/><br/>

**صُنع بـ ❤️ باستخدام [FastAPI](https://fastapi.tiangolo.com) • [React](https://react.dev) • [Playwright](https://playwright.dev)**

<br/>

[![Made with Python](https://img.shields.io/badge/صُنع%20بـ-Python-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Made with React](https://img.shields.io/badge/صُنع%20بـ-React-61dafb?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![Powered by FastAPI](https://img.shields.io/badge/يعمل%20بـ-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

<br/>

**© 2026 محمد عمر. جميع الحقوق محفوظة.**

</div>

</div>
