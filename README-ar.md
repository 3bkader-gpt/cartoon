<div align="center">

# ⚡ Cartoon Downloader

### ⚡ Lightning-Fast Media Downloader for Arabic Cartoons

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Latest-61DAFB.svg)](https://reactjs.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Latest-F7DF1E.svg)](https://www.javascript.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

**Download Entire Series • Fast & Efficient • Modern UI**

[المميزات](#-المميزات) • [التثبيت](#-التثبيت) • [الاستخدام](#-الاستخدام) • [المساهمة](#-المساهمة)

[العربية](#-cartoon-downloader) | [English](README.md)

</div>

---

## 📋 جدول المحتويات

- [نظرة عامة](#-نظرة-عامة)
- [المميزات](#-المميزات)
- [المتطلبات](#-المتطلبات)
- [التثبيت](#-التثبيت)
- [الإعدادات](#-الإعدادات)
- [الاستخدام](#-الاستخدام)
- [هيكل المشروع](#-هيكل-المشروع)
- [التقنيات المستخدمة](#-التقنيات-المستخدمة)
- [المساهمة](#-المساهمة)

---

## 🎯 نظرة عامة

**Cartoon Downloader** هو أداة سريعة وفعالة لتحميل مسلسلات الكرتون العربية بالكامل بنقرة واحدة. يدعم التحميل المجمع، واجهة مستخدم حديثة، وإدارة المكتبة.

### ✨ لماذا Cartoon Downloader؟

- ⚡ **سرعة فائقة** - تحميل سريع وفعال
- 📦 **تحميل مجمع** - تحميل مسلسل كامل بنقرة واحدة
- 🎨 **واجهة حديثة** - واجهة مستخدم جميلة وسهلة
- 📚 **إدارة المكتبة** - تنظيم وإدارة المحتوى المحمل

---

## 🌟 المميزات

### 🚀 المميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| ⚡ **تحميل سريع** | تحميل سريع وفعال للمسلسلات |
| 📦 **تحميل مجمع** | تحميل مسلسل كامل بنقرة واحدة |
| 🎨 **واجهة حديثة** | واجهة مستخدم جميلة وسهلة الاستخدام |
| 📚 **إدارة المكتبة** | تنظيم وإدارة المحتوى المحمل |
| 🔍 **بحث متقدم** | البحث عن المسلسلات بسهولة |
| 🎬 **دعم متعدد** | دعم Kodi و Plex |

### 🛠️ المميزات التقنية

- ✅ Full-Stack Application
- ✅ FastAPI Backend
- ✅ React Frontend
- ✅ SQLite Database
- ✅ Docker Support
- ✅ Web Scraping

---

## 📦 المتطلبات

قبل البدء، تأكد من تثبيت:

- **Python** 3.8 أو أحدث
- **Node.js** 16+ و npm
- **Docker** (اختياري للنشر)
- **Git**

---

## 🚀 التثبيت

### الطريقة الأولى: استخدام Docker (موصى به)

```bash
# 1. استنسخ المستودع
git clone https://github.com/3bkader-gpt/cartoon.git
cd cartoon

# 2. شغل باستخدام Docker Compose
docker-compose up -d

# 3. افتح المتصفح
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### الطريقة الثانية: التثبيت اليدوي

#### الخلفية (Backend)

```bash
cd backend

# أنشئ بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# ثبت المتطلبات
pip install -r requirements.txt

# شغل الخادم
uvicorn main:app --reload
```

#### الواجهة الأمامية (Frontend)

```bash
cd frontend

# ثبت المتطلبات
npm install

# شغل التطبيق
npm run dev
```

---

## ⚙️ الإعدادات

### متغيرات البيئة

أنشئ ملف `.env` في المجلد الرئيسي:

```env
# Backend
BACKEND_URL=http://localhost:8000

# Frontend
VITE_API_URL=http://localhost:8000

# Database
DATABASE_URL=sqlite:///./cartoon.db
```

---

## 📖 الاستخدام

### خطوات الاستخدام

1. ✅ **شغل التطبيق**
   ```bash
   docker-compose up -d
   ```

2. ✅ **افتح المتصفح**
   ```
   http://localhost:3000
   ```

3. ✅ **ابحث عن مسلسل**
   - استخدم شريط البحث
   - اختر المسلسل المطلوب

4. ✅ **حمّل المسلسل**
   - اضغط على زر التحميل
   - سيتم تحميل جميع الحلقات تلقائياً

### المميزات المتاحة

- 🔍 **البحث** - البحث عن المسلسلات
- 📥 **التحميل** - تحميل المسلسلات الكاملة
- 📚 **المكتبة** - عرض المحتوى المحمل
- ⚙️ **الإعدادات** - تخصيص الإعدادات

---

## 📁 هيكل المشروع

```
cartoon/
├── 📂 backend/              # API الخلفية (FastAPI)
│   ├── 📂 app/
│   ├── 📄 main.py
│   └── 📄 requirements.txt
├── 📂 frontend/              # الواجهة الأمامية (React)
│   ├── 📂 src/
│   └── 📄 package.json
├── 📂 docs/                  # الوثائق
├── 🐳 Dockerfile             # ملف Docker
├── 🐳 docker-compose.yml     # إعداد Docker Compose
└── 📄 README.md              # الوثائق
```

---

## 🛠️ التقنيات المستخدمة

### الخلفية (Backend)

<div align="center">

| التقنية | الوصف |
|---------|-------|
| ![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white) | لغة البرمجة الأساسية |
| ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi&logoColor=white) | إطار عمل الويب |
| ![Playwright](https://img.shields.io/badge/Playwright-Latest-45BA4B?logo=playwright&logoColor=white) | Web Scraping |
| ![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white) | قاعدة البيانات |

</div>

### الواجهة الأمامية (Frontend)

<div align="center">

| التقنية | الوصف |
|---------|-------|
| ![React](https://img.shields.io/badge/React-Latest-61DAFB?logo=react&logoColor=white) | مكتبة JavaScript |
| ![Vite](https://img.shields.io/badge/Vite-Latest-646CFF?logo=vite&logoColor=white) | Build Tool |
| ![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Latest-38B2AC?logo=tailwind-css&logoColor=white) | CSS Framework |

</div>

---

## 🚀 النشر

### Docker Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment

- **Render**: راجع ملف `render.yaml`
- **Heroku**: راجع ملف `Procfile`
- **Vercel**: للنشر السريع

---

## 🤝 المساهمة

نرحب بمساهماتك! 🎉

1. 🍴 Fork المشروع
2. 🌿 أنشئ فرع (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push (`git push origin feature/AmazingFeature`)
5. 🔄 افتح Pull Request

---

## 📄 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE) - راجع ملف LICENSE للتفاصيل.

---

## 📞 التواصل والدعم

- 🐛 **الإبلاغ عن مشاكل**: [افتح Issue](https://github.com/3bkader-gpt/cartoon/issues)
- 💡 **اقتراح ميزات**: [افتح Issue](https://github.com/3bkader-gpt/cartoon/issues)
- 📧 **البريد الإلكتروني**: medo.omar.salama@gmail.com

---

<div align="center">

**صُنع بـ ❤️ بواسطة [Mohamed Omar](https://github.com/3bkader-gpt)**

⭐ إذا أعجبك المشروع، لا تنسى إعطائه نجمة!

[⬆ العودة للأعلى](#-cartoon-downloader)

</div>