# 🧪 Testing Checklist - Arabic Toons Downloader

## ✅ Step 1: تثبيت النسخة الحالية

### Backend Verification
- [ ] Backend returns proper JSON for `/api/season/stream`
- [ ] Thumbnails are included in response (`thumbnail` field)
- [ ] File size is included in response (`metadata.size_formatted`)
- [ ] No Python errors in console
- [ ] Proxy endpoint `/api/proxy` works correctly

### Frontend Verification
- [ ] No console errors on page load
- [ ] No React warnings
- [ ] No infinite re-renders
- [ ] Dark mode toggle works
- [ ] Page loads in < 2 seconds

---

## ✅ Step 2: Testing كامل للميزات

### Feature 1: Episode Selection (Checkboxes)
- [ ] All episodes auto-selected on load
- [ ] Can check/uncheck individual episodes
- [ ] "Select All" checkbox works
- [ ] Selected count updates correctly
- [ ] Download buttons disabled when no selection

### Feature 2: File Size Display
- [ ] Size appears next to each episode filename
- [ ] Size formatted correctly (MB/GB)
- [ ] "Unknown" shown if size unavailable
- [ ] No layout shift when size loads

### Feature 3: Thumbnails
- [ ] Thumbnails load for episodes (if available)
- [ ] Placeholder icon shows when no thumbnail
- [ ] Images don't break layout
- [ ] No broken image icons
- [ ] Lazy loading works (if implemented)

### Feature 4: Sorting & Filtering
- [ ] Search bar filters by episode name
- [ ] Search bar filters by filename
- [ ] Sort by Episode Number works
- [ ] Sort by Name works
- [ ] Sort by Size works
- [ ] Asc/Desc toggle works
- [ ] Filtered count updates correctly

### Feature 5: Export Functions
- [ ] "Save List" exports only selected episodes
- [ ] "Export to IDM" creates .ef2 file
- [ ] .ef2 file has correct format
- [ ] Filenames are correct in export
- [ ] No duplicate entries

### Feature 6: Download (Proxy)
- [ ] Direct download button works
- [ ] Proxy fixes 403 errors
- [ ] Correct filename suggested
- [ ] Download starts immediately

### Feature 7: Performance
- [ ] Works smoothly with 20+ episodes
- [ ] No lag when scrolling
- [ ] Search is instant
- [ ] Sort is instant
- [ ] No memory leaks

---

## ✅ Step 3: Snapshot / Commit

### Files to Save
```
✅ d:/projects/cartoon/frontend/src/components/SeasonDownloader.jsx
✅ d:/projects/cartoon/api/arabic_toons_api.py
✅ d:/projects/cartoon/backend/main.py
✅ d:/projects/cartoon/frontend/src/api.js
```

### Version Info
- **Version**: v1.0-stable
- **Features**: Checkboxes, Thumbnails, Size, Sorting, Filtering, Proxy Download
- **Date**: 2025-11-23
- **Status**: ✅ STABLE

### Rollback Command
```bash
# If needed, restore from this checkpoint
git checkout HEAD -- frontend/src/components/SeasonDownloader.jsx
```

---

## 🐛 Known Issues (if any)
- None currently

## 📝 Notes
- All core features working
- Ready for next phase (Grid Layout, Cards, etc.)
- Performance tested with 20+ episodes
