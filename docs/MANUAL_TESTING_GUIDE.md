# 🧪 Manual Testing Guide - Step by Step

## 📋 Pre-Testing Setup

### 1. Start Backend
```bash
cd d:/projects/cartoon
python backend/main.py
```
**Expected**: Server running on `http://127.0.0.1:8000`

### 2. Start Frontend
```bash
cd d:/projects/cartoon/frontend
npm run dev
```
**Expected**: Dev server running on `http://localhost:5173`

### 3. Open Browser
Navigate to: `http://localhost:5173`

---

## ✅ Test 1: Initial Page Load

### Steps:
1. Open `http://localhost:5173`
2. Check browser console (F12)

### Expected Results:
- ✅ Page loads in < 2 seconds
- ✅ No console errors
- ✅ Input field visible
- ✅ "Fetch" button visible
- ✅ Dark mode toggle works

### Screenshot Checklist:
- [ ] Clean UI with no broken elements
- [ ] Placeholder text visible in input
- [ ] Button is styled correctly

---

## ✅ Test 2: Fetch Episodes

### Steps:
1. Paste a series URL (example: `https://www.arabic-toons.com/anime-streaming/...`)
2. Click "Fetch" button
3. Wait for progress bar

### Expected Results:
- ✅ Progress bar appears
- ✅ Percentage updates (0% → 100%)
- ✅ Episodes appear one by one
- ✅ No duplicate episodes
- ✅ All episodes auto-selected (checkboxes checked)

### Console Check:
- [ ] No errors in console
- [ ] Backend logs show successful requests

---

## ✅ Test 3: Episode Display

### For Each Episode, Verify:
- ✅ Checkbox is present and clickable
- ✅ Thumbnail loads OR placeholder shows
- ✅ Episode number badge visible
- ✅ Episode title displays correctly
- ✅ Filename shows below title
- ✅ File size appears (e.g., "250 MB")
- ✅ Hover shows action buttons (Copy, Download)

### Visual Check:
- [ ] No layout breaks
- [ ] Text doesn't overflow
- [ ] Images are properly sized (64x64px)

---

## ✅ Test 4: Selection System

### Test Cases:

#### 4.1 Individual Selection
1. Uncheck one episode
2. Check "selected count" updates

**Expected**: Count decreases by 1

#### 4.2 Select All Toggle
1. Click "Select All" checkbox
2. All episodes should deselect
3. Click again
4. All episodes should select

**Expected**: Toggle works both ways

#### 4.3 Filtered Selection
1. Search for specific episode
2. Click "Select All"
3. Only filtered episodes should be selected

**Expected**: Selection respects filter

---

## ✅ Test 5: Sorting & Filtering

### 5.1 Search Filter
1. Type "Episode 5" in search box
2. Only matching episodes show

**Expected**: Instant filtering, count updates

### 5.2 Sort by Episode
1. Select "Sort by Episode"
2. Click "↑ Asc"
3. Episodes in ascending order (1, 2, 3...)
4. Click "↓ Desc"
5. Episodes in descending order (10, 9, 8...)

**Expected**: Correct numerical sorting

### 5.3 Sort by Name
1. Select "Sort by Name"
2. Episodes sorted alphabetically

**Expected**: Alphabetical order

### 5.4 Sort by Size
1. Select "Sort by Size"
2. Episodes sorted by file size

**Expected**: Smallest → Largest (or reverse)

---

## ✅ Test 6: Export Functions

### 6.1 Save List (TXT)
1. Select 3 episodes
2. Click "Save List"
3. Open downloaded file

**Expected**:
- File named `episodes_list.txt`
- Contains 3 URLs (one per line)
- URLs are valid

### 6.2 Export to IDM
1. Select 5 episodes
2. Click "Export to IDM"
3. Open downloaded file

**Expected**:
- File named `season_export.ef2`
- Contains IDM format:
```
<
https://...video.mp4
filename=episode_1.mp4
>
```

---

## ✅ Test 7: Download (Proxy)

### Steps:
1. Hover over an episode
2. Click download button (green arrow)
3. Check if download starts

**Expected**:
- ✅ Download starts immediately
- ✅ Correct filename suggested
- ✅ No 403 Forbidden error
- ✅ File downloads successfully

### Verify:
- [ ] File size matches displayed size
- [ ] Video plays correctly

---

## ✅ Test 8: Copy URL

### Steps:
1. Hover over episode
2. Click copy button (blue clipboard)
3. Paste in notepad

**Expected**:
- ✅ Button shows checkmark briefly
- ✅ URL copied to clipboard
- ✅ URL is valid

---

## ✅ Test 9: Dark Mode

### Steps:
1. Toggle dark mode switch
2. Check all elements

**Expected**:
- ✅ Background changes to dark
- ✅ Text remains readable
- ✅ All colors adjust properly
- ✅ No white flashes

---

## ✅ Test 10: Responsive Design

### Steps:
1. Resize browser window
2. Test mobile view (F12 → Device Toolbar)

**Expected**:
- ✅ Layout adapts to screen size
- ✅ Buttons stack vertically on mobile
- ✅ Text remains readable
- ✅ No horizontal scroll

---

## 🐛 Edge Cases to Test

### Edge Case 1: No Episodes Found
1. Enter invalid URL
2. Click Fetch

**Expected**: Error message displays

### Edge Case 2: Missing Thumbnails
1. Fetch series with no images

**Expected**: Placeholder icons show

### Edge Case 3: Missing File Size
1. Episode without size metadata

**Expected**: Size field hidden or shows "Unknown"

### Edge Case 4: Very Long Episode Names
1. Find episode with long title

**Expected**: Text truncates with ellipsis (...)

### Edge Case 5: Special Characters
1. Episode with Arabic/special chars

**Expected**: Displays correctly, no encoding issues

---

## 📊 Performance Checks

### Check 1: Memory Usage
1. Open DevTools → Performance
2. Fetch 20+ episodes
3. Monitor memory

**Expected**: < 100MB RAM usage

### Check 2: Scroll Performance
1. Scroll through episode list
2. Check for lag

**Expected**: Smooth 60fps scrolling

### Check 3: Search Speed
1. Type in search box
2. Measure response time

**Expected**: < 100ms response

---

## ✅ Final Checklist

Before marking as STABLE:
- [ ] All 10 main tests passed
- [ ] All 5 edge cases handled
- [ ] Performance is acceptable
- [ ] No console errors
- [ ] No visual glitches
- [ ] Dark mode works perfectly
- [ ] Mobile view works
- [ ] All exports work correctly
- [ ] Downloads work without 403 errors
- [ ] Selection system is reliable

---

## 📝 Bug Report Template

If you find issues, document them:

```
Bug: [Short description]
Steps to Reproduce:
1. ...
2. ...
3. ...

Expected: [What should happen]
Actual: [What actually happened]
Console Errors: [Any errors]
Screenshot: [If applicable]
```

---

## ✅ Sign-Off

**Tester**: _____________  
**Date**: _____________  
**Status**: ⬜ PASS / ⬜ FAIL  
**Notes**: _____________

---

**Good luck with testing!** 🚀
