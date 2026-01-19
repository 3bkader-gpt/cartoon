<div align="center" dir="rtl">

<img src="docs/images/home.png" width="800" style="border-radius: 20px; box-shadow: 0 0 20px rgba(0,0,0,0.5);" alt="Arabic Toons Downloader" />

<br/><br/>

# 🎬 محمّل الكارتون العربي

### ⚡ أسرع أداة لتحميل الكارتون العربي

<p align="center">
  <a href="#-البدء-السريع">
    <img src="https://img.shields.io/badge/تحميل-v4.2.0-00d4ff?style=for-the-badge&logo=windows&logoColor=white&labelColor=1a1a2e" alt="تحميل" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/رخصة-MIT-f7df1e?style=for-the-badge&logo=star&logoColor=black&labelColor=1a1a2e" alt="رخصة" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776ab?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18+-61dafb?style=flat-square&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Playwright-Supported-2EAD33?style=flat-square&logo=playwright&logoColor=white" />
</p>

---

### 🚀 **حمّل مسلسلات كاملة بضغطة واحدة**
**تخزين ذكي • مكتبة شخصية • تصدير جاهز لـ Plex**

<br/>

</div>

<div dir="rtl">

## ✨ لماذا هذا التطبيق؟

<div align="center">

| ⚙️ **تحكم كامل** | ❤️ **تجربة رائعة** | 🚀 **سرعة فائقة** |
|:---:|:---:|:---:|
| **تسمية Plex**<br/>للخوادم المنزلية | **مكتبتي**<br/>حفظ المسلسلات | **تحميل دفعات**<br/>100+ حلقة فوراً |
| **تصدير مباشر**<br/>لبرنامج IDM / Aria2 | **وضع داكن**<br/>مريح للعين | **كاش ذكي**<br/>تخزين 24 ساعة |

</div>

---

## 📸 جولة بصرية

<table align="center" style="border: none;">
  <tr>
    <td align="center" width="33%">
      <img src="docs/images/library.png" style="border-radius: 10px; width: 100%;" />
      <br/><b>📚 مكتبتي</b>
    </td>
    <td align="center" width="33%">
      <img src="docs/images/settings.png" style="border-radius: 10px; width: 100%;" />
      <br/><b>⚙️ الإعدادات</b>
    </td>
    <td align="center" width="33%">
      <img src="docs/images/home.png" style="border-radius: 10px; width: 100%;" />
      <br/><b>📥 المحمّل</b>
    </td>
  </tr>
</table>

---

## 🚀 البدء السريع

<div align="center">

```bash
# 1. استنساخ المشروع
git clone https://github.com/3bkader-gpt/cartoon.git
cd cartoon

# 2. إعداد الخادم
pip install -r requirements.txt
playwright install chromium

# 3. إعداد الواجهة
cd frontend && npm install
```

**تشغيل التطبيق**

```bash
# Terminal 1             # Terminal 2
python backend/main.py   npm run dev
```

### [افتح التطبيق ↗](http://localhost:5173)

</div>

---

## 🏗️ تحت الغطاء

<details>
<summary><b>اضغط لرؤية المخطط المعماري</b></summary>
<br/>

```mermaid
graph TD
    User[👤 المستخدم] -->|يتفاعل| UI[⚛️ واجهة React]
    UI -->|طلبات API| API[⚡ خادم FastAPI]
    
    subgraph Backend Services
        API -->|فحص الكاش| DB[(🗄️ قاعدة بيانات SQLite)]
        API -->|جلب مباشر| Scraper[🔍 كاشط الويب]
        Scraper -->|Render| Browser[🎭 متصفح Playwright]
        
        DB -->|بيانات وصفية| API
        Browser -->|HTML| Scraper
    end
    
    subgraph Data Stores
        DB -- جدول المسلسلات --> Cache
        DB -- جدول المفضلة --> Library
    end
```

</details>

---

## 🗺️ خريطة الطريق

- [x] **v3.0** - المحمّل الأساسي (IndexedDB)
- [x] **v4.0** - الترحيل للخادم (SQLite)
- [x] **v4.1** - نظام المكتبة
- [x] **v4.2** - الإعدادات والتخصيص
- [ ] **v5.0** - **مدير التحميلات الداخلي** 🏗️
- [ ] **v6.0** - دعم مصادر متعددة 🔮

---

<div align="center">

### 👨‍💻 المطوّر

<a href="https://github.com/3bkader-gpt">
  <img src="https://img.shields.io/badge/محمد%20عمر-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="Mohamed Omar" />
</a>

<br/><br/>

إذا أعجبك المشروع، لا تبخل علينا بـ ⭐ **نجمة**!

<br/>

![Footer](https://capsule-render.vercel.app/api?type=waving&color=auto&height=100&section=footer)

</div>

</div>
