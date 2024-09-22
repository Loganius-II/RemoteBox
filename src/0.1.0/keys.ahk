; Get command-line arguments (input type and key)
InputType := A_Args[1] ; e.g., "keydown" or "keyup"
Key := A_Args[2] ; e.g., "A", "Backspace", "Enter", "Space", etc.

; Define special keys
Keyspecial := Map("Backspace", "{Backspace}",
    "Enter", "{Enter}",
    "Space", "{Space}",
    "LeftArrow", "{Left}",
    "RightArrow", "{Right}",
    "UpArrow", "{Up}",
    "DownArrow", "{Down}")


; Get the actual key to send
KeyToSend := Keyspecial[Key] ? Keyspecial[Key] : Key

; Automatically detect the active window if WinActive("A")
; "A" refers to the active window in AHK v2
if (WinActive("A")) {
    if (InputType = "keydown") {
        Send(KeyToSend "{Down}") ; Simulate key press
    } else if (InputType = "keyup") {
        Send(KeyToSend "{Up}") ; Simulate key release
    }
}

ExitApp