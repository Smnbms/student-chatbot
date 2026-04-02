
from flask import Flask, render_template, request, jsonify
import pickle
import difflib

# -----------------------------
# بارگذاری سوال‌ها و جواب‌ها
# -----------------------------
questions = pickle.load(open("questions_text.pkl", "rb"))
answers = pickle.load(open("answers.pkl", "rb"))
faq_dict = dict(zip(questions, answers))

# -----------------------------
# ساخت اپ Flask
# -----------------------------
app = Flask(__name__)

# -----------------------------
# صفحه اصلی (چت)
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------
# صفحه سوالات (جدید)
# -----------------------------
@app.route("/questions")
def questions_page():
    return render_template("questions.html", questions=questions)

# -----------------------------
# پاسخ چت‌بات
# -----------------------------
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get("message")

    if not user_input:
        return jsonify({"response": "لطفا یک سوال وارد کنید."})

    # پیام خوش‌آمدگویی
    if user_input.strip().lower() in ["سلام", "سلام!", "hi", "سلام چطوری؟"]:
        bot_response = (
            "سلام! من چت بات واحد آموزش دانشگاه هستم 🤖\n"
            "می‌تونم به سوالات متداول شما در حوزه ثبت‌نام، انتخاب واحد، قوانین آموزشی و درخواست‌ها پاسخ بدم."
        )
    else:
        matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)
        if matches:
            bot_response = faq_dict[matches[0]]
        else:
            bot_response = "متاسفم، سوال شما در دیتاست موجود نیست 😅 لطفا سوالت رو دقیق‌تر بیان کن."

    return jsonify({"response": bot_response})

# -----------------------------
# اجرای برنامه
# -----------------------------

if __name__=="__main__":
    app.run(debug=True)