# 🇮🇳 TaxWise India — Income Tax & Take-Home Simulator

A clean, interactive **Plotly Dash application** to simulate **income tax and net take-home salary** under the **Indian New Tax Regime (FY 2026–27)**.

Built for clarity, accuracy, and practical financial decision-making.

---

## 🚀 Features

* 📊 **Accurate Tax Engine**

  * Latest FY 2026–27 slabs (₹4L bands)
  * Progressive slab-wise computation
  * 4% cess included

* 💼 **Take-Home Salary Estimation**

  * PF contribution (realistic capped logic)
  * Custom deductions support
  * Monthly net income output

* 🎯 **Interactive Dashboard**

  * Built with Dash + Bootstrap
  * Responsive card-based UI
  * Clean visual hierarchy

* 🔍 **Transparent Tax Breakdown**

  * Slab-level tax visibility
  * Helps understand marginal vs effective tax

---

## 🧠 Tax Slabs (FY 2026–27)

| Income Range | Tax Rate |
| ------------ | -------- |
| 0 – 4L       | 0%       |
| 4 – 8L       | 5%       |
| 8 – 12L      | 10%      |
| 12 – 16L     | 15%      |
| 16 – 20L     | 20%      |
| 20 – 24L     | 25%      |
| Above 24L    | 30%      |

> ✔ Standard Deduction: ₹75,000
> ✔ Health & Education Cess: 4%

---

## 🏗️ Tech Stack

* **Dash (Plotly)** — Web framework
* **Dash Bootstrap Components** — UI system
* **Pandas / NumPy** — Tax computation engine

---

## 📦 Installation

```bash
git clone https://github.com/your-username/taxwise-india.git
cd taxwise-india

pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
python app.py
```

Open:

```
http://127.0.0.1:8050
```

---

## 📁 Project Structure

```
taxwise-india/
│
├── app.py                # Main Dash application
├── requirements.txt
├── README.md
│
├── src/
│   ├── tax_engine.py    # Core tax logic
│   ├── layout.py        # UI components
│   ├── callbacks.py     # App logic
│
└── assets/
    └── styles.css       # Custom styling
```

---

## 🔍 Example Scenario

**Input**

```
Basic + Allowances: ₹26,91,096
```

**Output**

```
Taxable Income: ₹26,16,096
Final Tax: ₹3,79,422
Monthly Take-Home: ~₹1.76L
```

---

## ⚙️ Core Concepts

### Progressive Taxation

Each slab is taxed independently — not the entire income.

### Marginal vs Effective Tax

* Marginal Tax Rate → 30%
* Effective Tax Rate → ~14–15%

---

## 🧩 Use Cases

* Salary negotiation planning
* Offer comparison (CTC vs net)
* Freelancing vs job decisions
* Financial literacy & tax understanding

---

## 🔮 Roadmap

* [ ] Old vs New regime comparison
* [ ] Income vs Tax visualization (Plotly)
* [ ] Multi-income support (salary + freelance)
* [ ] Investment planning (NPS, ELSS)
* [ ] Financial decision engine

---

## ⚠️ Disclaimer

This tool is for **educational and planning purposes only**.
Actual tax liability may vary based on:

* Employer structure
* Additional deductions
* Regulatory updates

---

## 📜 License

Apache License 2.0

---

## 👤 Author

**Vasant Rajadhyax**
Senior Data Scientist | ML Engineer

---

## ⭐ Contributions

Contributions are welcome.
Open an issue for discussion before major changes.

---

## 💡 Vision

Evolve **TaxWise India** into a **data-driven financial planning system**:

* Tax optimization
* Income strategy modeling
* AI-assisted financial insights

---
