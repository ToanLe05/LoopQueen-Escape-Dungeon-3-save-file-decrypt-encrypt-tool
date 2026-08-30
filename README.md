
# LoopQueen (Escape Dungeon 3) save file decrypt/encrypt tool

## Algorithm (extracted from Assembly-CSharp.dll, EncryptTools class):
    Cipher:  AES-256 (RijndaelManaged, 256-bit key)
    Mode:    ECB  (no IV)
    Padding: PKCS7
    Key:     UTF-8 bytes of the literal string
             "07872189057434672257123328872369"
    Wrapper: standard Base64 (Convert.ToBase64String / FromBase64String)

## Install dependency first:
    pip install pycryptodome
    pip install Crypto

## Usage:
    - To decrypt (first step):
```bash
python3 loopqueen_save_tool.py decrypt <in.json> [out.json]
```  
    - Exam the output json file, edit or do whatever you want.
    - To encrypt (final step):
```bash
python3 loopqueen_save_tool.py encrypt <in.json> [out.json]
```
## Example:
```bash
python3 loopqueen_save_tool.py decrypt data_a_user_game_data.json out.json
```
```bash
python3 loopqueen_save_tool.py encrypt out.json data_a_user_game_data.json
```

### decrypt: reads an encrypted save file, writes pretty-printed JSON.
### encrypt: reads pretty-printed (or minified) JSON, writes an encrypted
         save file in the game's format -- use this to write edited
         values back so the game will load them.

[!Warning]
Always back up your original save files before overwriting them.

---

*data_a_user_default.json* and *data_a_user_game_data.json* hold progress/stage state

*user_setting.json* holds options (language, volume, difficulty)

*user_memories.json* holds your unlocked-CG gallery flags

*user_game_log.json* is just a small log plus your Steam ID
