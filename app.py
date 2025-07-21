from flask import Flask
from flask import render_template
from flask import request
from dotenv import load_dotenv
import google.generativeai as genai
import os

app = Flask(__name__)

#load api keys from environment

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#serves home page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#serves converted page with endpoint done
@app.route('/done', methods=['GET', 'POST'])
def result():
    dropdown1_value = request.form.get('dropdown1') #saves choice of 1st dropdown from index.html
    dropdown2_value = request.form.get('dropdown2') #saves choice of 2nd dropdown from index.html
    same_value = dropdown1_value == dropdown2_value #bool variable checking if 1st (input lang) and 2nd (output lang) are same
    code = request.form['input-code'] #saves input code from index.html
    
    prompt = f"Convert this code from {dropdown1_value} to {dropdown2_value}. Output only the code, no explanations:\n{code}"
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    response = model.generate_content(prompt)
    answer = response.text.strip()
    
    return render_template('result.html', bool=same_value, in_opt=dropdown1_value, out_opt=dropdown2_value, input_code=code, output_code=answer)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, host='0.0.0.0', port=port)