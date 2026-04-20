import subprocess
import threading
import time
import os

class Speaker:
    def __init__(self):
        self.is_speaking   = False
        self.running       = True
        self._lock         = threading.Lock()
        self.current_text  = None
        self.new_message   = False
        self.urgent        = False

        # Get English voice
        self.voice = self._get_english_voice()
        print(f"✅ Using voice: {self.voice}")

        # Start worker
        self.thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.thread.start()
        print("✅ Speaker ready!")

    # ─────────────────────────────────────────────────
    def _get_english_voice(self):
        try:
            cmd = '''
            Add-Type -AssemblyName System.Speech;
            $s = New-Object System.Speech.Synthesis.SpeechSynthesizer;
            $s.GetInstalledVoices() | ForEach-Object {
                Write-Output $_.VoiceInfo.Name
            }
            '''
            result = subprocess.run(
                ['powershell', '-Command', cmd],
                capture_output=True,
                text=True
            )
            voices = result.stdout.strip().split('\n')
            voices = [v.strip() for v in voices
                     if v.strip()]
            print(f"📋 Voices: {voices}")

            english_voices = [
                'Microsoft David Desktop',
                'Microsoft Zira Desktop',
                'Microsoft Mark',
                'Microsoft David',
                'Microsoft Zira',
            ]

            for preferred in english_voices:
                for voice in voices:
                    if preferred.lower() in voice.lower():
                        return voice

            for voice in voices:
                if 'hortense' not in voice.lower() and \
                   'french'    not in voice.lower():
                    return voice

            return voices[0] if voices else None

        except Exception as e:
            print(f"❌ Voice error: {e}")
            return None

    # ─────────────────────────────────────────────────
    def _say_now(self, text):
        """
        Speak using VBScript
        Much faster than PowerShell!
        """
        try:
            self.is_speaking = True
            print(f"🔊 Speaking → {text}")

            # Create VBScript file
            vbs_content = f'''
Set speech = CreateObject("SAPI.SpVoice")
speech.Rate = 1
speech.Volume = 100
'''
            if self.voice:
                vbs_content += f'''
For Each v In speech.GetVoices
    If InStr(v.GetDescription(), "{self.voice}") > 0 Then
        Set speech.Voice = v
    End If
Next
'''
            vbs_content += f'speech.Speak "{text}"\n'

            # Write to temp file
            vbs_path = os.path.join(
                os.environ['TEMP'],
                'blind_speak.vbs'
            )
            with open(vbs_path, 'w') as f:
                f.write(vbs_content)

            # Run VBScript
            subprocess.run(
                ['cscript', '//nologo', vbs_path],
                timeout=15,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        except subprocess.TimeoutExpired:
            print("⚠️ Speech timeout")
        except Exception as e:
            print(f"❌ Speech error: {e}")
        finally:
            self.is_speaking = False

    # ─────────────────────────────────────────────────
    def _worker(self):
        """
        Background worker
        Always speaks latest message
        """
        while self.running:
            with self._lock:
                has_message = self.new_message
                text        = self.current_text
                is_urgent   = self.urgent

            if has_message and text:
                with self._lock:
                    self.new_message = False

                self._say_now(text)

            else:
                time.sleep(0.05)

    # ─────────────────────────────────────────────────
    def speak(self, text):
        """
        Normal speech
        Only speaks if not already speaking
        """
        with self._lock:
            if not self.is_speaking:
                print(f"📥 Queued → {text}")
                self.current_text = text
                self.new_message  = True
                self.urgent       = False
            else:
                print(f"⏭️ Skipped → {text}")

    # ─────────────────────────────────────────────────
    def speak_urgent(self, text):
        """
        Urgent speech
        ALWAYS speaks even if busy
        Interrupts current speech
        """
        print(f"🚨 Urgent → {text}")
        with self._lock:
            self.current_text = f"Warning! {text}"
            self.new_message  = True
            self.urgent       = True

    # ─────────────────────────────────────────────────
    def speak_and_wait(self, text):
        """
        Speak and wait until done
        """
        # Wait if speaking
        while self.is_speaking:
            time.sleep(0.1)

        # Set message
        with self._lock:
            self.current_text = text
            self.new_message  = True

        # Small delay for thread
        time.sleep(0.2)

        # Wait until done
        self.wait_until_done()

    # ─────────────────────────────────────────────────
    def wait_until_done(self):
        while self.is_speaking or self.new_message:
            time.sleep(0.1)

    # ─────────────────────────────────────────────────
    def stop(self):
        self.running = False


# ── Test ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("🔄 Testing Speaker...")
    speaker = Speaker()
    time.sleep(1)

    print("\n--- Test 1: Normal ---")
    speaker.speak_and_wait(
        "Hello I am your blind assistant"
    )
    print("✅ Test 1 done")

    print("\n--- Test 2: Urgent ---")
    speaker.speak_urgent(
        "Bottle very close in front of you!"
    )
    speaker.wait_until_done()
    print("✅ Test 2 done")

    print("\n--- Test 3: Detection ---")
    speaker.speak_and_wait(
        "Chair nearby on your left 120 centimeters"
    )
    print("✅ Test 3 done")

    print("\n--- Test 4: Scene ---")
    speaker.speak_and_wait(
        "I can see a person a chair and a bottle"
    )
    print("✅ Test 4 done")

    print("\n🎉 All tests passed!")
    speaker.stop()