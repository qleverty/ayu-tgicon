# Ayu-TGicon

Patches the icon straight into AyuGram's exe.

By default it swaps one of the built-in chibi icons for the classic Telegram logo.

<img src="https://github.com/qleverty/pics/raw/main/ayu-tgicon.png" width="200">

## Usage

1. Run `.PATCHER.exe`
2. Give it the path to your `AyuGram.exe` from [official releases](https://github.com/AyuGram/AyuGramDesktop/releases)
3. Get `AyuGram_patched.exe` right next to it

Taskbar icon updates instantly. If Explorer still shows the old file icon, run `clear icon cache.bat`.

Also, deleting `tdata` folder might be needed.

## Want a different icon instead

1. Run `converter.exe` and point it at any PNG
2. It spits out `override.png` and `override.ico`, sized to fit
3. Run the patcher

## How it works

AyuGram stores a couple of its icon assets uncompressed, right inside the exe. The patcher just finds those exact bytes and swaps them for new ones of the same size - nothing else in the binary gets touched.

## ⚠️ Warning!

Once patched, the original bytes are gone - running the patcher again on an already-patched exe won't find `original.ico`/`original.png` anymore, since they got replaced. Keep the original unpatched exe around if you want to change the icon again later.

---

Although it's made for AyuGram, nothing stops you using it for other situations, but I won't vouch for it there...
