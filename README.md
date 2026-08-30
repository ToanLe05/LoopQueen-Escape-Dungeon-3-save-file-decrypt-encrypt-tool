# LoopQueen (Escape Dungeon 3) save file decrypt/encrypt tool
---
> [!IMPORTANT]
> Extensive modification of the software directory may violate the developer's policies and terms; we accept no responsibility for any issues arising between you—the software user—and the distributor. Continue with your own risk.
---
The developers describe the content like this:
- This Game may contain content not appropriate for all ages, or may not be appropriate for viewing at work . The game contains Nudity or Sexual Content, Frequent Violence, sexual assault, non-consensual sex, BDSM, bestiality, sexual encounters with tentacles and monsters.
- All characters portrayed in this game are over the age of 20.
---
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
> [!CAUTION]
> Always back up your original save files before overwriting them.

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

- decrypt: reads an encrypted save file, writes pretty-printed JSON.
- encrypt: reads pretty-printed (or minified) JSON, writes an encrypted save file in the game's format -- use this to write edited values back so the game will load them.

---
## Supplementary Material 1

- Want to exam encrypt algorithm yourself?
  - Go to *Loop Queen-Escape Dungeon 3-1.5\\LoopQueen_Data\\Managed*
  - Open *Assembly-CSharp.dll* with a decompiler (dnSpy or ILSpy)
  - Look up *EncryptTools* class
  - The class looks kinda like this:
```cpp
public static class EncryptTools
{
    private static string key = "07872189057434672257123328872369"; // 32 chars = 256-bit key

    public static string Encrypt(string plainText)
    {
        var rijndael = new RijndaelManaged();
        rijndael.Key = Encoding.UTF8.GetBytes(key);
        rijndael.Mode = CipherMode.ECB;      // no IV needed
        rijndael.Padding = PaddingMode.PKCS7;
        var encryptor = rijndael.CreateEncryptor();
        return Convert.ToBase64String(encryptor.TransformFinalBlock(...));
    }
    // Decrypt is the exact mirror image
}
```
---
## Supplementary Material 2

*data_a_user_default.json* and *data_a_user_game_data.json* hold progress/stage state, 

*user_setting.json* holds options (language, volume, difficulty), 

*user_memories.json* holds your unlocked-CG gallery flags, 

*user_game_log.json* is just a small log plus your Steam ID.
