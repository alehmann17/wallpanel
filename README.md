# Wall Panel for iPad

A home dashboard with six screens. Swipe left or right, tap the menu at the bottom, or tap a card on
Home to open its screen:

- **Home**: the next 3 uptown 6 trains at Astor Place, today's weather with an hourly
  Temp / Rain / Feels chart, a Spotify mini player, today's calendar, and a word of the day.
- **Trains**: the next 8 uptown 6 trains.
- **Calendar**: today and tomorrow from Google Calendar.
- **Forecast**: **Day** (next 24 hours: temperature, rain chance, sunrise/sunset, plus feels-like,
  humidity, UV, wind, rain total and daylight) and **Week** (7 days with high/low bars on a shared scale).
- **Clock**: a big full-screen clock with the weather, the next uptown 6, and what's playing.
- **Music**: Spotify now playing, with album art and play/pause/skip.

Trains, Calendar and Forecast go back to Home after 3 minutes untouched.
The iPad fetches the MTA and weather data itself. No server, no API keys.

## Google Calendar setup (one time)
1. On a computer signed in to Google, go to script.google.com → **New project**.
2. Replace the code with the contents of `calendar-feed.gs` (in this folder) and click Save.
3. **Deploy → New deployment** → type **Web app**. Execute as **Me**, Who has access **Anyone**.
   Deploy, then allow access when Google asks.
4. Copy the **Web app URL** (ends in `/exec`) and paste it on the panel's Calendar screen.
   AirDrop it or use Universal Clipboard rather than typing it.

It shows events from the calendars that are ticked in Google Calendar. Anyone with the link can read
your next two days of events, so keep it private. To revoke it, delete the deployment
(Deploy → Manage deployments).

## Spotify setup (one time)
Spotify only works when the panel is opened from an **https://** address (for example GitHub Pages),
because sign-in uses the browser's secure crypto features.
1. On any computer, go to developer.spotify.com/dashboard, log in, and click **Create app**.
2. For **Redirect URI**, enter the panel's exact address. The Music screen shows it to you.
   Tick **Web API** and save.
3. Copy the app's **Client ID**, paste it on the Music screen, tap **Save**, then **Connect Spotify**.
Play/pause/skip need Spotify Premium. Showing what's playing works on free accounts.

The install steps below are for the old iOS 9 offline method. On iPadOS 17 or 18, host the
`public` folder on an https site instead, then use Add to Home Screen.

## One-time install (needs a computer for about 2 minutes)
1. On your Mac, in this folder, run:
       python3 server.py
   It prints an address like `http://192.168.1.20:8080`.
2. On the iPad (same Wi-Fi), open that address in Safari. Wait for it to fully load.
3. Tap Share → **Add to Home Screen**. Open the panel from the new icon once, with the Mac still running,
   so the full-screen app saves its own offline copy.
4. Stop the server (Ctrl-C). The panel keeps working.
5. iPad settings: Auto-Lock **Never**; Accessibility → **Guided Access** On. Then open the panel,
   triple-click Home, and tap Start.

To check that it really is standalone, turn the Mac off and force-quit and reopen the panel. It should load.

## Updating
Edit `public/index.html` or `public/words.js`, then change the `# v1` line in `public/panel.appcache`
(for example to `# v2`). Run `python3 server.py` and open the panel on the iPad. It picks up the new version
and reloads itself.

## Gotchas
- **Clearing Safari's history/website data** deletes the offline copy. Just repeat the install.
- Weather comes from Open-Meteo over plain `http://`, because iOS 9 doesn't trust its HTTPS certificate.
  It's public weather data, so being unencrypted is fine. The MTA feed uses HTTPS, which iOS 9 does trust.
- Trains auto-update every minute from 7:45 to 8:15am, then every 10 min until 10pm, then not at all until
  7:45am. **Refresh** fetches immediately at any time. Each MTA download is about 125 KB.
  Change the times with `RUSH_START`, `RUSH_END`, `QUIET_START` in `index.html`.

- The screen dims from 9pm to 6am. Tap anywhere to brighten it for a minute. A web page can't change
  the iPad's actual backlight, so for an even darker night, also lower the brightness in Control Center.
  Change the hours with `DIM_START` / `DIM_END` in `index.html`.
- Fonts (Manrope, Fraunces; both under the SIL Open Font License) are in `public/fonts` and saved offline with the page.

## Customize
- Stop / line: `STOP_ID` and `ROUTES` near the top of the script in `index.html`.
- Weather location: `latitude` / `longitude` in `WEATHER_URL`.
- Words: add entries to `public/words.js`.
