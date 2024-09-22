; Get command-line arguments (input type and key)
InputType := A_Args[1] ; e.g., "keydown" or "keyup"
Key := A_Args[2] ; e.g., "A", "1", "Backspace", "Enter", "Space", etc.
Casing := A_Args[3] ? A_Args[3] : "LowerCase"

; Define special keys using Map
Keyspecial := Map("Backspace", "{Backspace}",
    "Enter", "{Enter}",
    "Space", "{Space}",
    "Left", "{Left}",
    "Right", "{Right}",
    "Up", "{Up}",
    "Down", "{Down}",
    "LShift", "{LShift}")

; Handle alphanumeric keys (A-Z, 0-9)
if (Key ~= "^[A-Za-z0-9]$") {
    if (Casing = "UpperCase") {
    KeyToSend := Key
    } else {
    KeyToSend := StrLower(Key)
    }
} else {
    ; Get the actual key to send from the map, or use the key itself if not in map
    KeyToSend := Keyspecial.Has(Key) ? Keyspecial[Key] : Key
}

; Automatically detect the active window
if (WinActive("A")) {
    if (InputType = "keydown") {
        Send(KeyToSend "{Down}") ; Simulate key press
    } else if (InputType = "keyup") {
        Send(KeyToSend "{Up}") ; Simulate key release
    }
}

ExitApp