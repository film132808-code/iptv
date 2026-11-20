# 🌍 World IPTV Playlist — ⭐ 2,464 curated (master: 14,040)

**তৈরি: 20 নভেম্বর 2026** · সোর্স: [iptv-org](https://github.com/iptv-org/iptv) ওপেন-সোর্স পাবলিক চ্যানেল ডাটাবেজ (৭৬টি দেশ)

---

## 📂 ফাইলগুলো কী কী

| ফাইল | চ্যানেল | কী আছে |
|---|---|---|
| **`IPTV_World_VERIFIED.m3u`** | **6,994** | ✅ সবচেয়ে ভালো — শুধু যেসব লিংক টেস্টে **লাইভ** পাওয়া গেছে, দেশ অনুযায়ী গ্রুপ করা। **এটা দিয়ে শুরু করো।** |
| `IPTV_World_by_Country.m3u` | 9,546 | সম্পূর্ণ লিস্ট, দেশ অনুযায়ী গ্রুপ (verified + unverified সব) |
| `IPTV_World_by_Region.m3u` | 9,546 | একই চ্যানেল, কিন্তু Asia / Europe / Middle East / Americas / Africa ভাগে |
| `IPTV_World_by_Region_VERIFIED.m3u` | 6,994 | রিজিয়ন-গ্রুপড + শুধু লাইভ |
| `IPTV_South_Asia.m3u` | 1,063 | 🇧🇩 🇮🇳 🇵🇰 🇳🇵 🇱🇰 🇦🇫 🇲🇻 — সাউথ এশিয়া ফোকাস |
| `IPTV_South_Asia_VERIFIED.m3u` | 838 | সাউথ এশিয়া, শুধু লাইভ |

তোমার চাওয়া দেশগুলোর সংখ্যা: **বাংলাদেশ ৪৫ · ভারত ৮৩৬ · পাকিস্তান ১০৩ · যুক্তরাষ্ট্র ১,৫৫২ · যুক্তরাজ্য ২৯৬ · কানাডা ২১৭** — সাথে আরও ৭০টি দেশ।

লাইভ রেট: **৭৩%** (৯,৫৪৬ এর মধ্যে ৬,৯৯৪টি টেস্টের সময় রেসপন্স করেছে)।

---

## ▶️ কিভাবে চালাবে

### ১. VLC / মোবাইল প্লেয়ার দিয়ে (সবচেয়ে সহজ)
ফাইলটা ফোনে বা পিসিতে ডাউনলোড করো → VLC খোলো → **Playlist → Open file** → `.m3u` ফাইলটা সিলেক্ট করো।
(মোবাইলে VLC-এর Playlist ট্যাব থেকে ফাইল ইমপোর্ট করা যায়)

### ২. TiviMate / IPTV Smarters / OTT Navigator (অ্যান্ড্রয়েড টিভি, ফায়ারস্টিক)
এই অ্যাপগুলো সাধারণত **URL** চায়, ফাইল না। তাই:
1. ফাইলটা GitHub-এ (বা Dropbox/Google Drive-এ "direct link" হিসেবে) আপলোড করো
2. raw/direct লিংকটা কপি করো
3. TiviMate → **Add playlist → M3U playlist → URL** → লিংক পেস্ট করো

> টিপ: GitHub-এ ফ্রি রিপো বানিয়ে `IPTV_World_VERIFIED.m3u` আপলোড করলে
> `https://raw.githubusercontent.com/<তোমার-নাম>/<রিপো>/main/IPTV_World_VERIFIED.m3u`
> এই লিংকটা সরাসরি সব অ্যাপে কাজ করবে, আর আপডেটও সহজ।

### ৩. Kodi
Settings → PVR & Live TV → **PVR IPTV Simple Client** → M3U Play List URL-এ লিংক দাও → Enable।

### ৪. স্মার্ট টিভি (Samsung/LG)
যেসব অ্যাপ M3U সাপোর্ট করে (যেমন IPTV Smarters, SS IPTV) — সেখানে URL দিয়ে অ্যাড করো।

---

## ⚠️ গুরুত্বপূর্ণ কথা

- এগুলো **ফ্রি-টু-এয়ার / পাবলিকলি শেয়ারড স্ট্রিম**, কোনো পেইড সাবস্ক্রিপশন ক্র্যাক করা লিংক না। বাণিজ্যিক প্রিমিয়াম চ্যানেল (Star Sports, Sky Sports, HBO, Star Plus ইত্যাদি) এখানে **নেই** — ওগুলো কোথাও ফ্রি লিগ্যালি পাওয়া যায় না।
- **জিও-ব্লকিং**: অনেক চ্যানেল শুধু নিজের দেশ থেকে খোলে। বাংলাদেশ থেকে বসে US/UK-এর কিছু চ্যানেল নাও চলতে পারে — এটাই স্বাভাবিক, লিংক নষ্ট না।
- ফ্রি স্ট্রিম **প্রায়ই বন্ধ হয়ে যায়** বা সার্ভার বদলায়। তাই লিস্টটা প্রতি ১–২ সপ্তাহে রিফ্রেশ করা ভালো।
- কিছু চ্যানেল একই নামে দুবার থাকতে পারে (আলাদা সার্ভার) — যেটা চলে সেটা ব্যবহার করো।

---

## 🔄 লিস্ট আপডেট করার নিয়ম

এই ফোল্ডারে স্ক্রিপ্টগুলো আছে — ভবিষ্যতে নিজেই রিফ্রেশ করতে পারবে:

```bash
# ১) নতুন চ্যানেল নামাও
bash refresh.sh
# অথবা ধাপে ধাপে:
python3 build_playlist.py          # নতুন m3u বানায়
python3 check_streams.py IPTV_World_by_Country.m3u live_status.json   # লাইভ চেক (~২ মিনিট)
python3 make_verified.py           # verified ফাইল বানায়
```


---

## 🆕 নতুন সোর্স যোগ হয়েছে (v2)

প্রথম ভার্সনে শুধু **iptv-org** ছিল। এখন আরও দুটো ভিন্ন সোর্স যোগ করেছি:

| ফাইল | চ্যানেল | কী |
|---|---|---|
| **`IPTV_MASTER.m3u`** | **8,024** | ⭐ সব একসাথে — সব সোর্সের সম্পূর্ণ লিস্ট (নতুন + পুরোনো) |
| **`IPTV_BIG6.m3u`** | **2,527** | শুধু 🇧🇩 🇮🇳 🇵🇰 🇺🇸 🇬🇧 🇨🇦 — সবচেয়ে ছোট ফাইল, দ্রুত লোড হয় |
| `IPTV_Other_Sources_VERIFIED.m3u` | 983 | **Free-TV** প্রজেক্ট থেকে নতুন চ্যানেল, লাইভ-টেস্টেড |
| `IPTV_Other_Sources.m3u` | 1,497 | একই লিস্ট, ফিল্টার ছাড়া |
| `IPTV_YouTube_Live.m3u` | 47 | **অফিসিয়াল YouTube লাইভ** — Somoy TV, Jamuna TV, ATN News, Sky News, ABC, Al Jazeera... |

### 📺 YouTube লাইভ চ্যানেল (৪৭টি, ব্রডকাস্টারের নিজের চ্যানেল)

**বাংলাদেশ (২১):** Somoy TV · Jamuna TV · Independent TV · ATN News · ATN Bangla · DBC News · Ekattor TV · News24 · NTV · Channel i · Channel 24 · Bangla Vision · Maasranga · Rtv News · Nagorik TV · Shamol Bangla · Global TV · GTV · Deepto TV · T Sports · Maasranga News

**ভারত (১০):** Aaj Tak · India Today · NDTV · DD News · Zee News · ABP News · Republic Bharat · WION · CNBC-TV18 · Sansad TV

**পৃথিবী (১৬):** Sky News · ABC News · NBC News · PBS NewsHour · Bloomberg · CNBC · Al Jazeera (English + Arabic) · DW · Euronews · NHK World · CNA · Arirang · TRT World · CGTN · i24NEWS

> ⚠️ **YouTube লিংক নিয়ে সৎ কথা:** এগুলোর URL ফরম্যাট `youtube.com/channel/<id>/live` — সবসময় ওই চ্যানেলের চলমান লাইভ স্ট্রিমে নিয়ে যাবে, কখনো মরে না। কিন্তু **YouTube লিংক সব IPTV প্লেয়ারে চলে না** (TiviMate চলে না, VLC চলে না)। যেসব অ্যাপে চলে: **OTT Navigator**, **Kodi + YouTube plugin**, কিংবা ফোনে/পিসিতে লিংকটা সরাসরি YouTube অ্যাপে খুলে নাও — সবচেয়ে সহজ।
>
> টেকনিক্যাল কারণ: YouTube-এর নিজের HLS স্ট্রিমে অডিও আর ভিডিও আলাদা ট্র্যাকে আসে, আর লিংক ৬ ঘণ্টায় এক্সপায়ার হয় — তাই একে স্থায়ী `.m3u8` বানানো যায় না।

### 🆕 Free-TV সোর্স থেকে কী নতুন পেলাম

প্রথম ভার্সনে যেগুলো ছিল না — যেমন ইতালি, স্পেন, জার্মানির অনেক আঞ্চলিক চ্যানেল, আরব ও আফ্রিকান চ্যানেল, US-এর লোকাল স্টেশন, NHK World, TRT World, France 24, Euronews, News18, Russia 24 — মোট **১,৪৯৭টি নতুন লিংক**, যার **৯৮৩টি** লাইভ-টেস্টে কাজ করেছে (৬৬%)।

### 🔄 নতুন সোর্স আপডেট করতে
```bash
bash refresh_extras.sh     # Free-TV + YouTube রিফ্রেশ + সব ফাইল রিবিল্ড
bash refresh.sh            # শুধু iptv-org ভিত্তিক ফাইলগুলো রিফ্রেশ
```

### ❌ যেগুলো ইচ্ছাকৃতভাবে দিইনি
Star Sports, Sky Sports, HBO, Star Plus, Sony, Zee TV-এর মতো **পেইড/সাবস্ক্রিপশন চ্যানেল** — এগুলোর "ফ্রি" লিংক যেগুলো ইন্টারনেটে ঘোরে সেগুলো পাইরেসি, তাই সেগুলো যোগ করিনি। এই প্লেলিস্টের সবকিছুই ব্রডকাস্টারের নিজের পাবলিক/ফ্রি-টু-এয়ার স্ট্রিম।

---

## 🔴 Pluto TV — ৪৬৫টি ব্র্যান্ডেড চ্যানেল (ফ্রি ও লিগ্যাল)

তুমি যেহেতু "premium" চ্যানেল চেয়েছিলে, সবচেয়ে ভালো লিগ্যাল উত্তর হলো **Pluto TV** — Paramount-এর নিজস্ব ফ্রি সার্ভিস। এখানে সাবস্ক্রিপশন ছাড়াই বড় ব্র্যান্ডের চ্যানেল চলে (বিজ্ঞাপনসহ):

| ফাইল | চ্যানেল | |
|---|---|---|
| **`IPTV_PlutoTV_VERIFIED.m3u`** | **465** | ✅ ৪৬৫/৪৬৬টি টেস্টে কাজ করেছে (১০০%) |
| `IPTV_PlutoTV.m3u` | 466 | সম্পূর্ণ লিস্ট |

**যা পাবে:** CBS News 24/7 (+ ১৩টি লোকাল CBS স্টেশন), CNN Headlines, CNN Originals, BBC News, BBC Earth, Bloomberg TV+, CBS Sports HQ, Comedy Central, MTV, BET, Nick, Paramount Movie Channel, A&E Crime, Classic TV Comedy/Crime, Doctor Who, Baywatch, Top Gear — মোট ৪৬৫টি চ্যানেল, ২৫+ ক্যাটাগরিতে ভাগ করা।

> ⏳ **মেয়াদ:** Pluto-র প্রতিটি লিংকে একটা টোকেন থাকে যা **~২৪ ঘণ্টায় এক্সপায়ার হয়**। তাই মেয়াদ শেষে একটা কমান্ড চালাও:
> ```bash
> bash refresh_pluto.sh
> ```
> নতুন টোকেন নিয়ে ফাইল আবার তৈরি হয়ে যাবে (৩০ সেকেন্ডের কাজ)।

---

## ❌ GitHub-এর "premium IPTV" রিপো — কেন দিলাম না

তুমি GitHub-এর পাবলিক IPTV রিপো থেকে premium চ্যানেল নিতে বলেছিলে। সেগুলো আমি ইচ্ছাকৃতভাবে যোগ করিনি, তিনটা কারণে:

1. **এটা পাইরেসি।** Star Sports, Sky Sports, HBO, Star Plus, Sony, Zee TV, Ten Sports — এসব সাবস্ক্রিপশন-চ্যানেলের "ফ্রি" স্ট্রিম ব্রডকাস্টার ফাঁকি দিয়ে রিস্ট্রিম করা হয়। ওগুলো ব্যবহার করা এবং ছড়ানো আইনত লঙ্ঘন।
2. **ওগুলো আসলে কাজ করে না।** ওই রিপোগুলোর লিংক সাধারণত ২–৩ দিনে মরে যায়, কারণ সোর্স সাইট বন্ধ হয়ে যায় বা টোকেন বদলায়। "১০,০০০ premium চ্যানেল!" লেখা রিপোর ৯০%+ লিংক ডেড।
3. **নিরাপত্তা ঝুঁকি।** ওই ফ্রি "premium" প্লেলিস্টগুলোর সাথে ম্যালওয়্যার/ফিশিং সাইট, ক্রিপ্টো-স্ক্যাম অ্যাড, এমনকি ডিভাইসে স্ট্রিম রিপোর্ট পাঠানো ট্র্যাকারও থাকে।

**তোমার হাতে যা আছে সেটাই লিগ্যাল উপায়ে সবচেয়ে বেশি:** ৮,০২৪টি চ্যানেল + ৪৬৫টি Pluto ব্র্যান্ড চ্যানেল + ৪৭টি অফিসিয়াল YouTube লাইভ।

### সত্যিই premium চ্যানেল চাইলে
- **আইনগত উপায়:** যেকোনো IPTV প্রোভাইডার সাবস্ক্রিপশন (যেমন Toffee, Bioscope, Nagad/GP-এর বান্ডেল, অথবা আন্তর্জাতিকভাবে Sling/YouTube TV) — ওখানেই Star Sports, Sony, HBO আসলভাবে পাওয়া যায়
- **ফ্রি বিকল্প:** Pluto TV-তে CBS/CNN/BBC/Comedy Central আছে; BBC News, Al Jazeera, DW, NHK অফিসিয়াল স্ট্রিমে ফ্রি
- **খেলা:** T Sports (YouTube-এ ফ্রি), CBS Sports HQ (Pluto-তে ফ্রি), ফুটবল/ক্রিকেটের অফিসিয়াল ফ্রি হাইলাইটস

---

## 📡 আরও FAST সার্ভিস — চেষ্টার ফলাফল (সৎ রিপোর্ট)

তুমি Samsung TV Plus, Plex, Roku, Tubi যোগ করতে বলেছিলে। চারটাই চেষ্টা করেছি — ফলাফল মিশ্র:

| সার্ভিস | ফল | কারণ |
|---|---|---|
| **Pluto TV** | ✅ **465 চ্যানেল** | Pluto-র পাবলিক API ব্যবহার করে নিজে বানিয়েছি |
| **Samsung TV Plus** | ⚠️ আংশিক | ওদের API এখন কড়া ভ্যালিডেশন চায়, EPG ডেটা পেলেও স্ট্রিম URL পাইনি। iptv-org ইন্ডেক্সে যেগুলো ছিল সেগুলো নিয়েছি |
| **The Roku Channel** | ⚠️ আংশিক | স্ট্রিমের জন্য Roku অ্যাকাউন্ট টোকেন লাগে |
| **Plex Live TV** | ❌ | প্রতিটা রিকোয়েস্টে Plex টোকেন বাধ্যতামূলক (401 Unauthorized) |
| **Tubi** | ❌ | DRM (Widevine) দিয়ে সুরক্ষিত — M3U প্লেয়ারে চলে না |

> এগুলোর যেগুলো "ফ্রি" প্লেলিস্ট ইন্টারনেটে ঘোরে, সেগুলোতে অন্যের ব্যক্তিগত অ্যাকাউন্ট টোকেন ব্যবহার করা হয় — সেটা ঠিক না, তাই করিনি।

### যা নতুন পেলাম — পুরো iptv-org ইনডেক্স

শুধু দেশভিত্তিক প্লেলিস্ট না, iptv-org-এর **সম্পূর্ণ ইনডেক্স** (১১,৬৮১ চ্যানেল) থেকে বাকি সব বের করেছি:

| ফাইল | চ্যানেল | |
|---|---|---|
| **`IPTV_Index_Extra_VERIFIED.m3u`** | **1,387** | ✅ নতুন চ্যানেল, লাইভ-টেস্টেড |
| `IPTV_Index_Extra.m3u` | 2,000 | ফিল্টার ছাড়া |
| `IPTV_FAST_Extra.m3u` | 10 | Pluto/Samsung/Roku/Xumo/Plex-এর বাড়তি লিংক |

যা যোগ হলো: 🇺🇸 USA-তে +১৬১, 🇮🇳 ভারতে +২৫, 🇬🇧 UK-তে +১৩, 🇨🇦 Canada +২, আর ডমিনিকান রিপাবলিক, ভেনিজুয়েলা, কাজাকিস্তান সহ নতুন দেশ।

### 📊 এখন মোট

| ফাইল | চ্যানেল |
|---|---|
| **`IPTV_MASTER.m3u`** | **9,411** |
| **`IPTV_PlutoTV_VERIFIED.m3u`** | **465** |
| `IPTV_BIG6.m3u` (৬ দেশ) | 2,721 |
| `IPTV_YouTube_Live.m3u` | 47 |
| **সব মিলিয়ে** | **~9,900+** |

### 🔄 সব রিফ্রেশ করতে
```bash
bash refresh_pluto.sh      # Pluto (প্রতিদিন, টোকেন এক্সপায়ার হয়)
bash refresh_extras.sh     # Free-TV + YouTube
bash refresh.sh            # iptv-org মূল ফাইল
```

---

## 🗂 ক্যাটাগরি ভাগে ভাগ করা ফাইল

সব ফাইল `categories/` ফোল্ডারে। প্রতিটার `group-title`-এ ক্যাটাগরি নাম দেওয়া আছে, তাই প্লেয়ারে সুন্দর দেখাবে।

| ফাইল | চ্যানেল | কী আছে |
|---|---|---|
| `categories/News.m3u` | **984** | Somoy, Jamuna, ATN, BBC, CNN, Al Jazeera, Sky, NDTV, Aaj Tak... |
| `categories/Sports.m3u` | **365** | T Sports, CBS Sports HQ, Eurosport, Star/beIN-এর ফ্রি ফিড |
| `categories/Movies.m3u` | **768** | প্যারামাউন্ট মুভি চ্যানেল, বলিউড/হলিউড ফ্রি মুভি চ্যানেল |
| `categories/Entertainment.m3u` | **3,107** | সবচেয়ে বড় সেকশন — জেনারেল/সিরিজ/কমেডি চ্যানেল |
| `categories/Kids.m3u` | **479** | কার্টুন, Nick, Junior, বেবি চ্যানেল |
| `categories/Music.m3u` | **737** | MTV, হিটস, Dance, রিল্যাক্স/লো-ফাই মিউজিক |
| `categories/Documentary_and_Science.m3u` | **391** | BBC Earth, ডিসকভারি, হিস্ট্রি, নেচার |
| `categories/Religious.m3u` | **610** | কুরআন, ইসলামিক, আজান, ভক্তি চ্যানেল |
| `categories/Lifestyle_and_Travel.m3u` | **503** | ফুড, ট্রাভেল, অটো, হোম |
| `categories/Business.m3u` | **75** | Bloomberg, CNBC, মার্কেট চ্যানেল |
| `categories/Weather.m3u` | **21** | ওয়েদার/ক্লাইমেট চ্যানেল |
| `categories/Other.m3u` | **1,830** | যেগুলোর ক্যাটাগরি নির্ধারণ করা যায়নি |

**➕ সব ক্যাটাগরি একসাথে:** **`IPTV_By_Category.m3u`** — ৯,৮৭০টি চ্যানেল, ক্যাটাগরি অনুযায়ী গ্রুপ করা।

> 🎯 **মোট ৯,৮৭০টি চ্যানেল ১২টি ক্যাটাগরিতে ভাগ করা।** "Other"-এ ১,৮৩০টি আছে কারণ ওগুলোর নাম থেকে ক্যাটাগরি বোঝা যায় না (যেমন "9Gem", "7flix") — বেশিরভাগই অস্ট্রেলিয়া/আঞ্চলিক চ্যানেল।

### ব্যবহারের টিপস
- শুধু নিউজ দেখতে চাইলে **`categories/News.m3u`** লোড করো — ৯৮৪টি চ্যানেল, লোড হতে ২ সেকেন্ডও লাগবে না
- খেলা দেখতে **`categories/Sports.m3u`** (৩৬৫টি) — T Sports, CBS Sports HQ ফ্রি আছে
- বাচ্চাদের জন্য **`categories/Kids.m3u`** (৪৭৯টি)
- রিফ্রেশ: `bash refresh_categories.sh`

---

## 📡 FAST প্ল্যাটফর্ম — ৪,৬২৯টি নতুন লাইভ চ্যানেল ✅

তুমি যেটা চেয়েছিলে ("Toffee-র মতো ফ্রি সার্ভিস") — ঠিক সেই ধরনের সার্ভিসগুলো খুঁজে বের করেছি এবং কাজ করিয়েছি। এগুলো **বিজ্ঞাপন-ভিত্তিক ফ্রি (FAST)** সার্ভিস, সাবস্ক্রিপশন লাগে না, DRM নেই।

| সার্ভিস | লাইভ / মোট | লাইভ রেট | নোট |
|---|---|---|---|
| **Samsung TV Plus** | **2,477 / 2,652** | 93% | ১১টি দেশ — Kids, Movies, Crime, News, Sport ক্যাটাগরি |
| **Pluto TV** | **1,530 / 1,534** | 100% | ২০টি দেশ (US, UK, DE, IT, ES, FR, BR...) |
| **The Roku Channel** | **256 / 257** | 100% | US ফ্রি চ্যানেল |
| **Tubi** | **160 / 182** | 88% | A&E Crime 360, ABC News Live সহ |
| **Plex Live TV** | **206 / 2,890** | 7% | ⚠️ বেশিরভাগে Plex টোকেন লাগে, তাই কম |

**ফাইল:** `IPTV_FAST_Services_VERIFIED.m3u` (৪,৬২৯) · `IPTV_FAST_Services.m3u` (৭,৫১৫) · `IPTV_FAST_Services_VERIFIED.m3u`-তে প্রতি সার্ভিস আলাদা গ্রুপে।

### 🌍 রিজিয়ন কভারেজ
🇺🇸 USA · 🇬🇧 UK · 🇮🇳 India · 🇩🇪 Germany · 🇮🇹 Italy · 🇪🇸 Spain · 🇫🇷 France · 🇨🇭 Switzerland · 🇦🇹 Austria · 🇰🇷 Korea · 🇩🇰 Denmark · 🇸🇪 Sweden · 🇳🇴 Norway · 🇨🇦 Canada · 🇧🇷 Brazil

> 🇮🇳 **ভারতের Samsung TV Plus ৯৮% লাইভ (১৯৫টি চ্যানেল)** — বাংলাদেশ থেকে ভালোই চলবে!
> 🇩🇪 Germany ৯৭%, 🇮🇹 Italy ৯৬%, 🇰🇷 Korea ৯৯% — ইউরোপ/এশিয়ার লিংকগুলো সবচেয়ে স্ট্যাবল।

---

## 🔍 Toffee / Bioscope নিয়ে সত্যি কথাটা

তুমি জিজ্ঞেস করলে — "Toffee, Bioscope ফ্রি তাহলে ওদের চ্যানেল নাও না কেন?"

কারণ **"ফ্রি" আর "ফ্রি-টু-এয়ার" এক জিনিস না:**

| | Pluto / Samsung / Tubi | Toffee / Bioscope |
|---|---|---|
| খরচ | ফ্রি (বিজ্ঞাপন) | ফ্রি বা সাবস্ক্রিপশন |
| লাইসেন্স | প্ল্যাটফর্ম নিজেই চ্যানেল **টেলিকাস্ট করার অধিকার** কিনেছে | একই — কিন্তু স্ট্রিম **DRM দিয়ে লক** |
| প্রযুক্তি | খোলা HLS স্ট্রিম, যেকোনো প্লেয়ারে চলে | **Widevine DRM** + অ্যাপ-লকড |
| বাইরে থেকে ব্যবহার | বৈধ, কাজ করে | টোকেন ভাঙা = পাইরেসি, তার উপর কার্যত অসম্ভব |

Toffee-র Star Sports বা Bioscope-র HBO স্ট্রিম বের করতে হলে ওদের DRM ভাঙতে হবে — সেটা শুধু বেআইনি না, **প্রযুক্তিগতভাবেও সম্ভব না** (প্রতিটা প্লেয়ারে ডিভাইস-লেভেল সার্টিফিকেট লাগে)।

**তাই আসল সমাধান:** ওই ধরনের কনটেন্ট যেসব সার্ভিস বৈধভাবে ফ্রি দেয় — সেগুলো নিয়েছি (উপরের টেবিল)। Toffee/Bioscope ব্যবহার করতে চাইলে ওদের **অ্যাপ দিয়েই** দেখো, সেটাই বৈধ ও নিরাপদ।

---

## 🎯 এখন তোমার সম্পূর্ণ কালেকশন

| ফাইল | চ্যানেল |
|---|---|
| **`IPTV_MASTER.m3u`** | **14,040** |
| **`IPTV_FAST_Services_VERIFIED.m3u`** | **4,629** |
| `IPTV_By_Category.m3u` | 14,499 |
| `IPTV_BIG6.m3u` (৬ দেশ) | 4,737 |
| `IPTV_PlutoTV_VERIFIED.m3u` | 465 |
| `IPTV_YouTube_Live.m3u` | 47 |

**ক্যাটাগরি (নতুন সংখ্যা):** News **1,301** · Sports **802** · Movies **1,217** · Entertainment **4,309** · Music **966** · Documentary & Science **897** · Kids **653** · Lifestyle **748** · Religious **614** · Business **85**

### 🔄 রিফ্রেশ
```bash
bash refresh_fast.sh      # Samsung/Plex/Pluto/Roku/Tubi + মাস্টার + ক্যাটাগরি
bash refresh_pluto.sh     # নিজের Pluto (প্রতিদিন)
bash refresh_categories.sh
```

---

## ⭐ `IPTV_POPULAR.m3u` — ছোট, কিউরেটেড, ডাবল-ফিল্টার (এটাই এখন ব্যবহার করো)

**২,৪৬৪টি চ্যানেল** — ১৪,০৪০ থেকে ৮২% কম। শুধু সেই চ্যানেলগুলো রাখা হয়েছে যেগুলো মানুষ সত্যিই দেখে।

### 🔎 Country + Category দুভাবেই ফিল্টার করা যায়

প্রতিটা গ্রুপের নাম এই ফরম্যাটে:

```
🇧🇩 Bangladesh · 📰 News
🇮🇳 India · ⚽ Sports
🇺🇸 United States · 🎬 Movies
```

তাই TiviMate / OTT Navigator-এ **গ্রুপ সার্চ বক্সে "Bangladesh" লিখলে** দেশের সব চ্যানেল, আর **"News" লিখলে** সব দেশের নিউজ — দুটোই পাওয়া যাবে। মোট **৪৩৬টি গ্রুপ**।

### 📊 জনপ্রিয়তা কীভাবে মাপা হয়েছে

আসল ভিউয়ারশিপ ডেটা কারও কাছে公开 নেই, তাই দুটো বাস্তব সংকেত ব্যবহার করেছি:

1. **একই চ্যানেল কতগুলো আলাদা সোর্সে আছে** — BBC, CNN, Somoy-এর মতো বড় চ্যানেল অনেক প্লেলিস্টে থাকে, ছোট চ্যানেল একটায়। এটাই সবচেয়ে নির্ভরযোগ্য সূচক।
2. **ব্র্যান্ড তালিকা** — ২০০+ পরিচিত চ্যানেলের নাম (BBC, CNN, Al Jazeera, NDTV, Somoy, Jamuna, Discovery...) সরাসরি চিহ্নিত।

তারপর প্রতি দেশে একটা সীমা (US ২৬০, India ২০০, UK ১৬০, Bangladesh ৬০...) রেখে বেছে নেওয়া হয়েছে, যাতে একটা দেশ পুরো লিস্ট দখল না করে।

### 🎬 পুরনো ভুল ঠিক করা হয়েছে
পেইড চ্যানেলের (Star Jalsha, Zee Bangla, Sony, HBO, Cartoon Network) **১৭২টি "ফ্রি" লিংক** বাদ দিয়েছি — ওগুলো লাইসেন্সড চ্যানেলের পাইরেটেড রিস্টিম। শুধু যে পেইড ব্র্যান্ডগুলো **Pluto/Samsung-এর মতো লাইসেন্সপ্রাপ্ত প্ল্যাটফর্ম** থেকে আসছে সেগুলো রাখা হয়েছে।

---

## ▶️ YouTube চ্যানেলগুলোর আসল সমাধান

তুমি ঠিক ধরেছ — **YouTube লিংকগুলো চলে না**। কারণটা এখন প্রমাণসহ জানি:

> yt-dlp দিয়ে পরীক্ষা করে দেখেছি — YouTube লাইভ স্ট্রিমে **ভিডিও আর অডিও আলাদা ট্র্যাকে** আসে (`video only` + `audio only`), একসাথে muxed ট্র্যাক দেয় না। কোনো IPTV প্লেয়ার একসাথে দুটো ট্র্যাক মেলাতে পারে না — তাই ছবি আসে নাই অডিও আসে।

**যেগুলোর বিকল্প পাওয়া গেছে (৩১টি) — সব YouTube লিংক সরিয়ে আসল HLS দেওয়া হয়েছে:**

| YouTube | প্রতিস্থাপিত HLS |
|---|---|
| Aaj Tak, NDTV, India Today, Zee News, ABP, Republic, WION, DD News, CNBC-TV18 | ✅ আসল HLS |
| Sky News, ABC News, NBC News, Euronews, NHK World, TRT World, CGTN | ✅ আসল HLS |
| Al Jazeera English, DW News, Arirang, CNA, PBS | ✅ আসল HLS |

**যেগুলোর কোনো HLS নেই (১৫টি) — শুধু YouTube-এ আছে:**

| চ্যানেল | |
|---|---|
| **SOMOY TV, Jamuna TV, Ekattor TV, ATN News, DBC News, Independent TV, Channel 24, Rtv News, Nagorik TV, Shamol Bangla, Maasranga, Channel i, Deepto TV, T Sports, ATN Bangla** | ⚠️ |

এগুলো বাংলাদেশের টিভি চ্যানেল — ওরা **শুধু YouTube-এই** ফ্রি লাইভ দেয়, নিজস্ব কোনো HLS স্ট্রিম নেই (ওয়েবসাইটেও YouTube embed করা)। তাই M3U-তে এগুলোর কোনো বৈধ সোর্স নেই। এগুলো `[YT]` ট্যাগ দিয়ে চিহ্নিত — YouTube অ্যাপে দেখো, ওখানে হুবহু একই সম্প্রচার ফ্রি।

**বাংলাদেশ সেকশনে এখন ৩৩টি চ্যানেল** — ১৮টি আসল HLS (NTV, Bangla Vision, Boishakhi, Channel S, Ekushey, Azan TV...), ১৫টি `[YT]`।

---

## 📋 কোন ফাইল কখন ব্যবহার করবে

| পরিস্থিতি | ফাইল |
|---|---|
| **সাধারণ ব্যবহার (সবচেয়ে ভালো)** | ⭐ `IPTV_POPULAR.m3u` — 2,464 |
| সব চ্যানেল চাই | `IPTV_MASTER.m3u` — 14,040 |
| শুধু একটা ক্যাটাগরি | `categories/News.m3u` ইত্যাদি |
| শুধু FAST প্ল্যাটফর্ম | `IPTV_FAST_Services_VERIFIED.m3u` — 4,629 |
| ৬টি দেশ | `IPTV_BIG6.m3u` — 4,737 |

### 🔄 রিফ্রেশ
```bash
bash refresh_popular.sh    # কিউরেটেড লিস্ট রিবিল্ড (ক্যাটাগরি সহ)
```

---

## 🇧🇩 `IPTV_Bangla_Bollywood.m3u` — বাংলা ও বলিউড (৪৩টি চ্যানেল, সব বৈধ)

তুমি Star Jalsha, Zee Bangla, Sony, HBO চেয়েছিলে। সেগুলোর পাইরেটেড লিংক দিইনি, কিন্তু তোমার আসল চাহিদা — **বাংলা বিনোদন** — বৈধভাবে যতটা পাওয়া যায় সব এনেছি:

**🇮🇳 Samsung TV Plus India থেকে (লাইসেন্সপ্রাপ্ত):**
- **News18 Bangla** 📰 · **TV9 Bangla** 📰 · **R Bangla** 🎭 · **Sangeet Bangla** 🎵
- **B4U Movies** 🎬 · **B4U Kadak** 🎬 · **Bollywood Masala** 🎬 · **B4U Music** 🎵

**🇧🇩 বাংলাদেশের ফ্রি-টু-এয়ার (১৮টি আসল HLS):**
NTV · Bangla Vision · Boishakhi TV · Channel S · Aamar Bangla · Ananda TV · Deshi TV · Nexus TV · Rajdhani TV · Ekushey TV · Probashi TV · News 21 Bangla · NAN TV · Matribhumi TV · Azan TV · Madani Channel Bangla · Movie Bangla

---

## ✅ Star Jalsha / Zee Bangla / Sony / HBO — বৈধ উপায় (বাংলাদেশে)

এই চ্যানেলগুলো **সাবস্ক্রিপশন চ্যানেল** (Tata Play-র রেট কার্ডে "Pay" লেখা, মাসে ₹১৫-২০ করে লাইসেন্স ফি)। ইন্টারনেটে এগুলোর যেকোনো "ফ্রি" লিংক = অনুমতিহীন রিস্টিম।

**কিন্তু বাংলাদেশে এগুলো বৈধভাবে সস্তায় পাওয়া যায়:**

| চ্যানেল | বৈধ উৎস | খরচ |
|---|---|---|
| **Star Jalsha, Jalsha Movies, Star Plus, Star Gold, Star Bharat, Nat Geo** | **Toffee** (toffeelive.com / অ্যাপ) | ফ্রি-তে শুরু, কিছু প্যাক পেইড |
| **Zee Bangla, Sony Ten Sports 1/2 HD** | **Toffee** | একই |
| **HBO** | HBO Max বাংলাদেশে নেই; Amazon Prime Video-তে কিছু HBO সিরিজ | Prime সাবস্ক্রিপশন |
| **Sony (SET, SAB, Sony Aath)** | SonyLIV / Toffee | সাবস্ক্রিপশন |

> 📌 Toffee-তে Star Channels আসার খবরটি [ঢাকা ট্রিবিউনে প্রকাশিত](https://www.dhakatribune.com/showtime/304544/star-channels-now-available-at-toffee) — Star Plus, Star Gold, Star Bharat, Star Jalsha, Jalsha Movies, National Geographic, Fox Life, Nat Geo Wild সবই আছে।
>
> **Toffee পুরোপুরি বৈধ ও ফ্রি-তে শুরু করা যায়** — এটাই তোমার জন্য সবচেয়ে ভালো সমাধান। ওদের অ্যাপ/সাইটে গেলে Star Jalsha-র আসল লাইভ স্ট্রিম পাবে, কোনো ঝুঁকি ছাড়া।

### ❌ কেন পাইরেটেড লিংক দিলাম না
1. **আইনত** — লাইসেন্সপ্রাপ্ত কনটেন্ট অনুমতি ছাড়া বিতরণ করা অপরাধ
2. **ব্যবহারিক** — ওই "ফ্রি" লিংক ২-৩ দিনে মরে যায়, কারণ সোর্স সার্ভার বন্ধ হয়ে যায়
3. **নিরাপত্তা** — ওই সার্ভারগুলোতে ম্যালওয়্যার ও ফিশিং থাকে; অনেক ক্ষেত্রে তোমার IP/ডিভাইস ডেটা সংগ্রহ করে

---

## 📋 ফাইল গাইড (আপডেটেড)

| ফাইল | চ্যানেল | কখন |
|---|---|---|
| ⭐ `IPTV_POPULAR.m3u` | 2,464 | **সাধারণ ব্যবহার — এটাই শুরু করো** |
| 🇧🇩 `IPTV_Bangla_Bollywood.m3u` | 43 | শুধু বাংলা + বলিউড |
| `IPTV_MASTER.m3u` | 14,040 | সব |
| `IPTV_FAST_Services_VERIFIED.m3u` | 4,629 | Samsung/Pluto/Roku/Tubi |
| `categories/News.m3u` | 1,301 | শুধু নিউজ |

---

## 📊 দেশভিত্তিক চ্যানেল সংখ্যা

| Country | Ch | Country | Ch | Country | Ch | Country | Ch |
|---|---|---|---|---|---|---|---|
| United States | 1552 | India | 836 | Russia | 505 | Brazil | 391 |
| Italy | 359 | Spain | 336 | Germany | 301 | United Kingdom | 296 |
| France | 224 | Argentina | 219 | Canada | 217 | Romania | 201 |
| Chile | 200 | Poland | 187 | Peru | 185 | Turkey | 175 |
| Ukraine | 175 | Indonesia | 172 | Iran | 172 | Mexico | 170 |
| Netherlands | 170 | Hungary | 157 | Denmark | 151 | China | 150 |
| Colombia | 150 | Sweden | 136 | Norway | 112 | Czechia | 107 |
| Pakistan | 103 | Vietnam | 90 | Bulgaria | 80 | South Korea | 71 |
| Thailand | 71 | Greece | 68 | Portugal | 67 | Australia | 65 |
| Slovakia | 62 | Iraq | 58 | Saudi Arabia | 53 | Nigeria | 51 |
| Bangladesh | 45 | Kenya | 38 | Belgium | 37 | Serbia | 34 |
| Austria | 33 | Switzerland | 32 | Taiwan | 32 | Croatia | 27 |
| Lithuania | 27 | Cambodia | 25 | Finland | 24 | Albania | 22 |
| Slovenia | 21 | South Africa | 21 | UAE | 20 | Egypt | 19 |
| Hong Kong | 18 | New Zealand | 18 | Afghanistan | 17 | Myanmar | 17 |
| Sri Lanka | 17 | Bosnia | 16 | Japan | 16 | Philippines | 15 |
| Latvia | 14 | Nepal | 14 | Ireland | 13 | Morocco | 12 |
| Kuwait | 11 | Maldives | 10 | Qatar | 9 | Singapore | 9 |
| Malaysia | 5 | Oman | 5 | Bahrain | 4 | Iceland | 4 |

---

## 🔗 URL বানানো ও রেগুলার আপডেট

👉 **সম্পূর্ণ গাইড: [`PUBLISH.md`](PUBLISH.md)**

সংক্ষেপে: এই স্যান্ডবক্সের সার্ভার স্থায়ী না, তাই **GitHub-এ ফ্রি হোস্ট** করো —

```
https://raw.githubusercontent.com/<তোমার-নাম>/iptv/main/IPTV_POPULAR.m3u
https://cdn.jsdelivr.net/gh/<তোমার-নাম>/iptv@main/IPTV_POPULAR.m3u   ← দ্রুততর
```

**অটো-আপডেট:** `.github/workflows/update.yml` ফাইলটা রিপোতে থাকলে GitHub **প্রতিদিন সকাল ৮টায় (ঢাকা)** নিজেই সব সোর্স ডাউনলোড করে, প্রতিটা চ্যানেল লাইভ টেস্ট করে, মৃত লিংক বাদ দিয়ে নতুন ফাইল কমিট করবে। URL একই থাকবে, ভেতরটা অটো আপডেট।

**নিজে রিফ্রেশ করতে:** `bash update_all.sh` (৫-৮ মিনিট, সব ফাইল রিবিল্ড)
