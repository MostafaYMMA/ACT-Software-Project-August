# Tasks Page Search & Date Filter Implementation Guide

## 📋 Overview

The Tasks page has been completely updated to use a backend-powered search and filtering system. Users can now search for tasks by title, description, and project reference, filter by date ranges, and combine filters together for precise task discovery.

## 🚀 Features Implemented

### 1. Backend-Connected Search
- **Text Search**: Search across task title, description, and source reference fields
- **Debounced Input**: 300ms debounce prevents excessive API calls while typing
- **Full Database Search**: Searches the entire task database, not just loaded tasks
- **Combined Filters**: Works seamlessly with date filters and status tabs

### 2. Date Filtering
- **Quick Presets**:
  - Today
  - Yesterday
  - Last 7 days
  - Last 30 days
- **Custom Date Range**: 
  - From date picker
  - To date picker
  - Apply and Clear buttons
- **ISO Format**: Uses YYYY-MM-DD format for compatibility with backend

### 3. Status Tabs
- **All**: Display all tasks regardless of status
- **Open**: Display unfinished/unassigned tasks
- **Completed**: Display completed tasks (when backend supports)
- **Combination**: Works with search and date filters

### 4. UI/UX Improvements
- **Loading States**: Shows "Loading tasks..." while fetching from API
- **Empty States**: Context-aware messages for each tab and filter combination
- **Error Handling**: Graceful error messages if API fails
- **Responsive Design**: Works on desktop and mobile devices
- **Consistent Styling**: Maintains ACT orange branding throughout

## 📁 Files Modified

### Backend Files

#### `backend/repositories/task_repository.py`
```python
def search_tasks(
    search_query: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    status: str | None = None,
) -> list[dict]:
```
- Added new search function
- Supports text search across multiple fields
- Supports date range filtering
- Supports status filtering

#### `backend/services/task_service.py`
```python
def search_tasks(
    search_query: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    status: str | None = None,
) -> list[dict]:
```
- Added service layer wrapper for search

#### `backend/api/v1/routers/tasks.py`
```python
@router.get("")
def list_tasks(
    current_pm: PM = Depends(get_current_pm),
    search: str | None = Query(None),
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    status: str | None = Query(None),
):
```
- Updated endpoint to accept query parameters
- Automatically uses search if any filter provided
- Full documentation in docstring

### Frontend Files

#### `frontend/tasks.html`
- **Added**: Date filter UI component with popover menu
- **Added**: Inline script using backend API for task fetching
- **Updated**: Search bar styling to work with date filter button
- **Removed**: References to localStorage task storage
- **Added**: Loading state indicator
- **Features**:
  - Debounced search input
  - Date preset buttons
  - Custom date range picker
  - Real-time filter updates
  - Error handling

#### `frontend/css/style.css`
- **Added**: `.date-filter-popover` styles with animation
- **Added**: `.date-preset` button styling
- **Added**: Task row and task list item styling
- **Added**: Loading state styling
- **Enhanced**: Button and input styling for consistency

## 🔌 API Contract

### Endpoint
```
GET /api/v1/tasks?search=<query>&from_date=<date>&to_date=<date>&status=<status>
```

### Query Parameters
| Parameter | Type | Format | Example |
|-----------|------|--------|---------|
| `search` | string | Text query | `onboarding` |
| `from_date` | string | YYYY-MM-DD | `2026-08-01` |
| `to_date` | string | YYYY-MM-DD | `2026-08-18` |
| `status` | string | assigned/unassigned | `assigned` |

### Response Format
```json
[
  {
    "id": 1,
    "title": "Review pull request #114",
    "description": "Code review for feature branch",
    "status": "assigned",
    "assigned_pm_id": 123,
    "source_email_id": "project@example.com",
    "source_reference": "PR-114",
    "created_at": "2026-08-18T10:00:00Z",
    "updated_at": "2026-08-18T10:00:00Z"
  }
]
```

### Example Requests
```bash
# Search for tasks
GET /api/v1/tasks?search=onboarding

# Date range filter
GET /api/v1/tasks?from_date=2026-08-01&to_date=2026-08-18

# Combined filters
GET /api/v1/tasks?search=onboarding&from_date=2026-08-01&to_date=2026-08-18

# Status filter
GET /api/v1/tasks?status=assigned
```

## ✅ Testing Checklist

### Basic Functionality
- [ ] Load tasks page without filters - displays all tasks
- [ ] Search bar appears with placeholder text
- [ ] Date filter button is visible and clickable
- [ ] Tabs (All/Open/Completed) are present and functional

### Text Search
- [ ] Type in search box - results update after 300ms
- [ ] Search by task title - finds matching tasks
- [ ] Search by description - finds matching tasks
- [ ] Search by reference number - finds matching tasks
- [ ] Multiple word search - finds tasks with all words
- [ ] Search with no results - shows "No tasks found" message
- [ ] Clear button appears and clears search

### Date Filtering
- [ ] Date filter menu opens on button click
- [ ] Today preset - shows today's tasks
- [ ] Yesterday preset - shows yesterday's tasks
- [ ] Last 7 days preset - shows last week's tasks
- [ ] Last 30 days preset - shows last month's tasks
- [ ] Custom range toggle opens date pickers
- [ ] From date picker selects date
- [ ] To date picker selects date
- [ ] Apply button applies custom range
- [ ] Clear button removes date filter
- [ ] Date label updates to show active filter

### Combined Filters
- [ ] Search + date range works together
- [ ] Search + preset date works together
- [ ] Tab selection + search works together
- [ ] Tab selection + date range works together
- [ ] All three filters (tab + search + date) work together

### Status Tabs
- [ ] All tab shows all tasks
- [ ] Open tab filters correctly
- [ ] Completed tab filters correctly
- [ ] Switching tabs updates results
- [ ] Tab + search combination works
- [ ] Tab + date filter combination works

### UI/UX
- [ ] Loading state appears while fetching
- [ ] Error message appears on API failure
- [ ] Empty state message is appropriate for context
- [ ] Responsive layout on mobile
- [ ] Search bar is accessible
- [ ] Date filter menu is accessible
- [ ] Buttons have hover states
- [ ] Date inputs work on all browsers

### Edge Cases
- [ ] Very long search query - handles gracefully
- [ ] Special characters in search - escapes properly
- [ ] Empty result set - shows appropriate message
- [ ] API timeout - shows error message
- [ ] Page refresh with active filters - maintains filter state (if needed)
- [ ] Rapid filter changes - debounces properly
- [ ] Switching between date presets - updates correctly

### Performance
- [ ] Type fast in search box - doesn't spam API calls
- [ ] Switch tabs quickly - handles race conditions
- [ ] Apply multiple filters - responsive performance
- [ ] Results load within 1 second
- [ ] No memory leaks on repeated searches
- [ ] Smooth animations and transitions

## 🔧 How It Works

### Frontend Flow
1. User loads Tasks page → `fetchTasks()` called to load initial tasks
2. User types in search → `onSearchInput()` debounces 300ms → `fetchTasks()`
3. User opens date filter → popover menu displays
4. User selects preset → `applyDatePreset()` → `updateDateFilterLabel()` → `fetchTasks()`
5. User clicks tab → `onTabClick()` → `fetchTasks()`
6. API returns data → `applyStatusFilter()` filters by tab → `renderTasks()` displays results

### Backend Flow
1. Request arrives at `/api/v1/tasks` endpoint
2. Query parameters extracted: search, from_date, to_date, status
3. If any filter provided → call `task_service.search_tasks()`
4. Service calls `task_repository.search_tasks()`
5. Repository:
   - Queries Supabase with date filters
   - Client-side filters text search results
   - Returns matching tasks
6. Results serialized as JSON and sent to frontend

## 📝 Important Notes

### Date Format
- Always use ISO format: **YYYY-MM-DD**
- Frontend date picker automatically converts to this format
- Backend expects dates in this format in query parameters

### Status Values
- Current backend supports: `assigned`, `unassigned`
- "Completed" tab is ready for when backend adds completion tracking
- Tab filtering is client-side after API returns results

### Search Behavior
- Case-insensitive search
- Searches across: title, description, source_reference
- Client-side filtering for flexibility
- Non-invasive - doesn't modify stored data

### Performance Considerations
- Search is debounced 300ms to prevent API spam
- Date filters are applied server-side via Supabase queries
- Text search is client-side filtered for flexibility
- All filtering is stateless - can be combined in any way

### Authentication
- Requires valid authentication token in localStorage
- Token passed as Bearer token in Authorization header
- 405 Method Not Allowed errors indicate missing OPTIONS support (expected for GET with Query params)

## 🐛 Troubleshooting

### No tasks showing
- Check browser console for API errors
- Verify authentication token is set
- Check backend is running on port 8000
- Verify frontend can reach backend (check CORS if needed)

### Search not working
- Check API response in Network tab
- Verify search terms match task data (case-insensitive)
- Ensure no typos in query parameters

### Date filter not working
- Verify dates are in YYYY-MM-DD format
- Check date range doesn't have from_date > to_date
- Ensure tasks have created_at timestamps

### Slow performance
- Check API response time in Network tab
- Reduce date range to fewer tasks
- Check database indices on created_at field

## 📞 Future Enhancements

- Add sorting options (by date, priority, title)
- Add pagination for large result sets
- Add saved filters/views
- Add filter history
- Add export functionality
- Add task count in filter labels
- Add visual indicators for active filters
- Add keyboard shortcuts for common filters

## ✨ Summary

The Tasks page is now fully powered by the backend API with rich search and filtering capabilities. Users can find tasks quickly using text search, date ranges, and status filters, all working together seamlessly. The implementation maintains the existing design while adding modern filtering UI that's intuitive and responsive.
