import customtkinter as ctk
from tkinter import filedialog, messagebox
import requests
import re
import threading
from bs4 import BeautifulSoup
from datetime import datetime


# =====================================================================
#  Appearance & Theme
# =====================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Element Scraper")
        self.root.geometry("900x800")
        self.root.minsize(700, 600)

        # ------------------------------------------------------------------
        #  Grid configuration
        # ------------------------------------------------------------------
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # ------------------------------------------------------------------
        #  Main scrollable frame
        # ------------------------------------------------------------------
        self.main_frame = ctk.CTkScrollableFrame(root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # ------------------------------------------------------------------
        #  Title
        # ------------------------------------------------------------------
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="🖥️  HTML Element Scraper",
            font=ctk.CTkFont(size=22, weight="bold"))
        title_label.grid(row=0, column=0, pady=(5, 15), sticky="w")

        # ------------------------------------------------------------------
        #  URL input
        # ------------------------------------------------------------------
        url_label = ctk.CTkLabel(
            self.main_frame, text="URL:",
            font=ctk.CTkFont(size=13, weight="bold"))
        url_label.grid(row=1, column=0, pady=(0, 3), sticky="w")

        self.url_entry = ctk.CTkEntry(
            self.main_frame,
            font=ctk.CTkFont(size=13),
            height=38,
            placeholder_text="https://example.com/video-page")
        self.url_entry.grid(row=2, column=0, pady=(0, 12), sticky="ew")

        # ------------------------------------------------------------------
        #  Pattern input (multi-line)
        # ------------------------------------------------------------------
        pattern_label = ctk.CTkLabel(
            self.main_frame, text="Patterns (one per line):",
            font=ctk.CTkFont(size=13, weight="bold"))
        pattern_label.grid(row=3, column=0, pady=(0, 3), sticky="w")

        help_text = (
            "┌─────────────────────────────────────────────────────────────────┐\n"
            "│  Supported pattern formats:                                      │\n"
            "│  • JS Call:    html5player.setVideoUrlHigh()                    │\n"
            "│  • HTML Tag:   <video src>  or  <source src>                    │\n"
            "│  • Tag.Attr:   video.src  or  source.src                        │\n"
            "│  • Attribute:  data-src  or  data-video-url                     │\n"
            "└─────────────────────────────────────────────────────────────────┘"
        )
        help_label = ctk.CTkLabel(
            self.main_frame, text=help_text,
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="gray60", justify="left")
        help_label.grid(row=4, column=0, pady=(0, 5), sticky="w")

        self.pattern_textbox = ctk.CTkTextbox(
            self.main_frame,
            height=110,
            font=ctk.CTkFont(family="Consolas", size=12))
        self.pattern_textbox.grid(row=5, column=0, pady=(0, 12), sticky="ew")

        # ------------------------------------------------------------------
        #  Buttons
        # ------------------------------------------------------------------
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.grid(row=6, column=0, pady=(0, 10), sticky="ew")

        self.scrape_btn = ctk.CTkButton(
            btn_frame, text="🔍  Scrape", command=self.start_scraping,
            font=ctk.CTkFont(size=13, weight="bold"), height=36, width=120)
        self.scrape_btn.pack(side="left", padx=(0, 8))

        self.save_btn = ctk.CTkButton(
            btn_frame, text="💾  Save to File", command=self.save_to_file,
            font=ctk.CTkFont(size=13), height=36, width=130)
        self.save_btn.pack(side="left", padx=8)

        self.copy_btn = ctk.CTkButton(
            btn_frame, text="📋  Copy", command=self.copy_results,
            font=ctk.CTkFont(size=13), height=36, width=90)
        self.copy_btn.pack(side="left", padx=8)

        self.clear_btn = ctk.CTkButton(
            btn_frame, text="🗑  Clear", command=self.clear_all,
            font=ctk.CTkFont(size=13), height=36, width=90,
            fg_color="#dc3545", hover_color="#c82333")
        self.clear_btn.pack(side="left", padx=8)

        self.example_btn = ctk.CTkButton(
            btn_frame, text="📝  Examples", command=self.load_examples,
            font=ctk.CTkFont(size=13), height=36, width=110)
        self.example_btn.pack(side="left", padx=8)

        # ------------------------------------------------------------------
        #  Results
        # ------------------------------------------------------------------
        results_label = ctk.CTkLabel(
            self.main_frame, text="Results:",
            font=ctk.CTkFont(size=13, weight="bold"))
        results_label.grid(row=7, column=0, pady=(5, 3), sticky="w")

        self.results_textbox = ctk.CTkTextbox(
            self.main_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            height=350,
            wrap="word")
        self.results_textbox.grid(row=8, column=0, pady=(0, 10), sticky="nsew")
        self.main_frame.grid_rowconfigure(8, weight=1)

        # ------------------------------------------------------------------
        #  Status bar
        # ------------------------------------------------------------------
        self.status_label = ctk.CTkLabel(
            root, text=" Ready",
            anchor="w",
            font=ctk.CTkFont(size=11),
            text_color="gray70")
        self.status_label.grid(row=1, column=0, sticky="ew", padx=20,
                               pady=(0, 10))

    # ==================================================================
    #  Pattern type detection
    # ==================================================================

    def detect_pattern_type(self, pattern):
        """
        Detect pattern type and return a tuple (type, tag, attr).
        Types:
          - 'js_call'     : html5player.setVideoUrlHigh()
          - 'html_tag'    : <video src>
          - 'tag_attr'    : video.src
          - 'attribute'   : data-src
        """
        p = pattern.strip()

        # ── JS function call ──────────────────────────────────────────
        if '()' in p or re.search(r'\([^)]*\)\s*$', p):
            return ('js_call', None, None)

        # ── HTML tag with attribute:  <video src>  ────────────────────
        if p.startswith('<'):
            inner = p.rstrip('>').lstrip('<').strip()
            parts = inner.split()
            if len(parts) >= 2:
                return ('html_tag', parts[0], parts[1])
            elif len(parts) == 1:
                return ('html_tag', parts[0], None)
            else:
                return ('unknown', None, None)

        # ── tag.attr:  video.src  ─────────────────────────────────────
        if '.' in p and not p.startswith('.'):
            parts = p.split('.', 1)
            return ('tag_attr', parts[0], parts[1])

        # ── standalone attribute:  data-src  ──────────────────────────
        return ('attribute', None, p)

    # ==================================================================
    #  Extraction logic per pattern type
    # ==================================================================

    def extract_js_call(self, html, pattern):
        """Extract values from JS function calls like func('value')."""
        base = pattern.strip()
        if base.endswith('()'):
            base = base[:-2]

        escaped = re.escape(base)
        regex = escaped + r"\(\s*(?:['\"]([^'\"]*)['\"]|([^)]+?))\s*\)"

        matches = re.findall(regex, html)
        results = []
        for m in matches:
            val = m[0] if m[0] else m[1].strip()
            results.append(val)
        return results

    def extract_html_tag(self, html, tag, attr):
        """Extract attribute values from HTML tags like <video src='...'>."""
        if not attr:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for el in soup.find_all(tag):
            if el.has_attr(attr):
                results.append(el[attr])
        return results

    def extract_tag_attr(self, html, tag, attr):
        """Extract attribute values using tag.attr notation."""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for el in soup.find_all(tag):
            if el.has_attr(attr):
                results.append(el[attr])
        return results

    def extract_attribute(self, html, attr):
        """Extract values from any tag that has the given attribute."""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for el in soup.find_all(attrs={attr: True}):
            results.append(el[attr])
        return results

    def extract_pattern(self, html, pattern):
        """Master dispatcher: detect pattern type and call the right extractor."""
        ptype, tag, attr = self.detect_pattern_type(pattern)

        if ptype == 'js_call':
            return self.extract_js_call(html, pattern)
        elif ptype == 'html_tag':
            return self.extract_html_tag(html, tag, attr)
        elif ptype == 'tag_attr':
            return self.extract_tag_attr(html, tag, attr)
        elif ptype == 'attribute':
            return self.extract_attribute(html, attr)
        else:
            return []

    # ==================================================================
    #  Scraping orchestration
    # ==================================================================

    def start_scraping(self):
        """Launch scrape in a background thread so the GUI stays responsive."""
        self.scrape_btn.configure(state="disabled", text="⏳  Scraping...")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("end", "Scraping, please wait...\n")
        self.status_label.configure(text=" ⏳ Scraping...")

        thread = threading.Thread(target=self._scrape, daemon=True)
        thread.start()

    def _scrape(self):
        url = self.url_entry.get().strip()
        patterns_text = self.pattern_textbox.get("1.0", "end").strip()

        if not url or not patterns_text:
            self.root.after(0, lambda: messagebox.showwarning(
                "Input Error", "Please provide both URL and at least one pattern."))
            self.root.after(0, self._reset_scrape_button)
            return

        patterns = [line.strip() for line in patterns_text.splitlines()
                    if line.strip()]

        try:
            headers = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/120.0.0.0 Safari/537.36')
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            html = response.text

            all_results = {}
            for pat in patterns:
                ptype, tag, attr = self.detect_pattern_type(pat)
                results = self.extract_pattern(html, pat)
                all_results[pat] = {
                    'type': ptype,
                    'tag': tag,
                    'attr': attr,
                    'results': results
                }

            self.root.after(0, lambda: self._display_results(all_results))

        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: self._show_error("Network Error", str(e)))
        except Exception as e:
            self.root.after(0, lambda: self._show_error("Error", str(e)))

    # ==================================================================
    #  Result display
    # ==================================================================

    def _display_results(self, all_results):
        self.results_textbox.delete("1.0", "end")

        total_matches = 0
        output_lines = []

        for pattern, data in all_results.items():
            ptype = data['type']
            results = data['results']
            count = len(results)
            total_matches += count

            # Pattern type badge
            type_emoji = {
                'js_call': '⚙️',
                'html_tag': '🏷️',
                'tag_attr': '🔗',
                'attribute': '📌',
                'unknown': '❓'
            }.get(ptype, '❓')

            # Header
            output_lines.append(f"{'═' * 70}")
            output_lines.append(f"  {type_emoji}  Pattern: {pattern}")
            output_lines.append(f"     Type: {ptype}")

            if data['tag']:
                output_lines.append(f"     Tag:  {data['tag']}")
            if data['attr']:
                output_lines.append(f"     Attr: {data['attr']}")

            output_lines.append(f"     Found: {count} match(es)")
            output_lines.append(f"{'─' * 70}")

            if results:
                for i, r in enumerate(results, 1):
                    output_lines.append(f"  [{i}] {r}")
            else:
                output_lines.append("  (no matches found)")

            output_lines.append("")

        self.results_textbox.insert("end", "\n".join(output_lines))

        status = f" ✅ Completed — {total_matches} total match(es) across {len(all_results)} pattern(s)"
        self.status_label.configure(text=status)
        self._reset_scrape_button()

    def _reset_scrape_button(self):
        self.scrape_btn.configure(state="normal", text="🔍  Scrape")

    def _show_error(self, title, message):
        self.results_textbox.delete("1.0", "end")
        messagebox.showerror(title, message)
        self.status_label.configure(text=f" ❌ {title}")
        self._reset_scrape_button()

    # ==================================================================
    #  File operations
    # ==================================================================

    def save_to_file(self):
        content = self.results_textbox.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Empty", "No results to save.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"scrape_results_{timestamp}.txt"

        filepath = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ])

        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_label.configure(text=f" 💾 Saved to {filepath}")
                messagebox.showinfo("Success", f"Results saved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def copy_results(self):
        content = self.results_textbox.get("1.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.status_label.configure(text=" 📋 Results copied to clipboard")

    def clear_all(self):
        self.url_entry.delete(0, "end")
        self.pattern_textbox.delete("1.0", "end")
        self.results_textbox.delete("1.0", "end")
        self.status_label.configure(text=" Ready")

    def load_examples(self):
        """Load example patterns into the pattern textbox."""
        examples = (
            "html5player.setVideoUrlHigh()\n"
            "html5player.setVideoUrlLow()\n"
            "<video src>\n"
            "<source src>\n"
            "video.src\n"
            "data-src\n"
            "data-video-url"
        )
        self.pattern_textbox.delete("1.0", "end")
        self.pattern_textbox.insert("1.0", examples)
        self.status_label.configure(text=" 📝 Example patterns loaded")


# =====================================================================
#  Main entry point
# =====================================================================
if __name__ == "__main__":
    root = ctk.CTk()
    app = WebScraperApp(root)
    root.mainloop()