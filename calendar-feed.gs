/**
 * Calendar feed for the wall panel.
 *
 * Paste this into a new Google Apps Script project (script.google.com → New project), then
 * Deploy → New deployment → type "Web app" → Execute as: Me → Who has access: Anyone → Deploy.
 * Copy the Web app URL (ends in /exec) and paste it on the panel's Calendar screen.
 *
 * It returns today's and tomorrow's events from the calendars you have switched on (ticked) in
 * Google Calendar, as JSON. Anyone who has the URL can read those two days of events, so treat
 * the URL like a password. To revoke it, delete the deployment (Deploy → Manage deployments).
 */
function doGet() {
  var start = new Date();
  start.setHours(0, 0, 0, 0);
  var end = new Date(start.getTime() + 2 * 24 * 60 * 60 * 1000);   // today + tomorrow
  var events = [];

  CalendarApp.getAllCalendars().forEach(function (cal) {
    if (!cal.isSelected() || cal.isHidden()) return;   // only calendars ticked in Google Calendar
    cal.getEvents(start, end).forEach(function (ev) {
      var allDay = ev.isAllDayEvent();
      events.push({
        title: ev.getTitle() || '(No title)',
        start: (allDay ? ev.getAllDayStartDate() : ev.getStartTime()).getTime(),
        end: (allDay ? ev.getAllDayEndDate() : ev.getEndTime()).getTime(),
        allDay: allDay,
        location: ev.getLocation() || '',
        calendar: cal.getName(),
        color: cal.getColor()
      });
    });
  });

  events.sort(function (a, b) { return a.start - b.start; });
  return ContentService
    .createTextOutput(JSON.stringify({ events: events, generated: Date.now() }))
    .setMimeType(ContentService.MimeType.JSON);
}
