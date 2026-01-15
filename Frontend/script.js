// DOM Elements
const circle = document.getElementById('risk-ring');
const riskPercentageText = document.getElementById('risk-percentage');
const riskStatusTag = document.getElementById('risk-status');
const predictionText = document.getElementById('pred-text');
const confidenceInner = document.getElementById('confidence-inner');
const churnSubmitBtn = document.getElementById('churnSubmitBtn');

// Progress Ring Logic
const radius = circle ? circle.r.baseVal.value : 80;
const circumference = radius * 2 * Math.PI;

if (circle) {
    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference;
}

/**
 * Updates the visual progress ring and color coding
 * @param {number} percent 
 */
function setProgress(percent) {
    if (!circle) return;
    const offset = circumference - (percent / 100 * circumference);
    circle.style.strokeDashoffset = offset;

    // Smooth Color Transition
    if (percent > 70) circle.style.stroke = 'var(--danger)';
    else if (percent > 40) circle.style.stroke = 'var(--warning)';
    else circle.style.stroke = 'var(--success)';
}

/**
 * Tab Switching Logic
 * @param {'loyalty' | 'allowance'} tab 
 */
function showTab(tab) {
    const loyaltySection = document.getElementById('loyalty-section');
    const allowanceSection = document.getElementById('allowance-section');
    const tabLoyalty = document.getElementById('tab-loyalty');
    const tabAllowance = document.getElementById('tab-allowance');

    loyaltySection.classList.toggle('hidden', tab !== 'loyalty');
    allowanceSection.classList.toggle('hidden', tab !== 'allowance');
    tabLoyalty.classList.toggle('active', tab === 'loyalty');
    tabAllowance.classList.toggle('active', tab === 'allowance');

    // Reset Display
    updateUI(0, 'Waiting for input', 'Enter data to see analysis.', 'moderate');
}

/**
 * Updates Global UI Components
 */
function updateUI(prob, statusText, predText, statusClass) {
    if (riskPercentageText) riskPercentageText.innerText = prob + '%';
    setProgress(prob);
    if (predictionText) predictionText.innerText = predText;
    if (riskStatusTag) {
        riskStatusTag.innerText = statusText;
        riskStatusTag.className = 'status-tag ' + statusClass;
    }
    if (confidenceInner) confidenceInner.style.width = prob + '%';
}

/**
 * Submit Churn Prediction
 */
async function submitChurn(e) {
    e.preventDefault();

    const payload = {
        CustomerId: document.getElementById('customerId').value,
        Age: parseFloat(document.getElementById('loyaltyAge').value),
        CreditScore: parseFloat(document.getElementById('loyaltyCreditScore').value),
        Tenure: parseFloat(document.getElementById('loyaltyTenure').value),
        TransactionFrequency: parseFloat(document.getElementById('transactionFrequency').value),
        AvgTransactionAmount: parseFloat(document.getElementById('avgTransactionAmount').value),
        ComplaintsFiled: parseFloat(document.getElementById('complaintsFiled').value),
        CustomerSatisfaction: parseFloat(document.getElementById('customerSatisfaction').value),
        HasLoan: document.getElementById('hasLoan').checked,
        Balance: parseFloat(document.getElementById('balance').value)
    };

    try {
        if (churnSubmitBtn) churnSubmitBtn.innerText = 'Analyzing Hub...';

        const response = await fetch('http://127.0.0.1:8000/predict_churn', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('API Error');

        const result = await response.json();
        updateUI(result.probability, result.risk_level + " Risk", result.prediction, result.risk_level.toLowerCase());

    } catch (err) {
        console.error(err);
        alert("Connectivity Error: Ensure FastAPI server is running on port 5000");
    } finally {
        if (churnSubmitBtn) churnSubmitBtn.innerText = 'Analyze Risk';
    }
}

/**
 * Submit Allowance Prediction
 */
async function submitAllowance(e) {
    e.preventDefault();

    const payload = {
        CreditScore: parseFloat(document.getElementById('allowanceCreditScore').value),
        Gender: document.getElementById('gender').value,
        Age: parseFloat(document.getElementById('allowanceAge').value),
        Tenure: parseFloat(document.getElementById('allowanceTenure').value),
        Balance: parseFloat(document.getElementById('allowanceBalance').value),
        NumOfProducts: parseFloat(document.getElementById('numOfProducts').value),
        HasCrCard: document.getElementById('hasCrCard').checked,
        IsActiveMember: document.getElementById('isActiveMember').checked,
        EstimatedSalary: parseFloat(document.getElementById('estimatedSalary').value)
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/predict_allowance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('API Error');

        const result = await response.json();

        const statusClass = result.status === 'Elite' ? 'low' : result.status === 'Standard' ? 'moderate' : 'critical';
        updateUI(result.probability, result.status + " Score", result.prediction, statusClass);

    } catch (err) {
        console.error(err);
        alert("Connectivity Error: Ensure FastAPI server is running on port 5000");
    }
}

// Global scope attachment for HTML inline attributes
window.showTab = showTab;
window.submitChurn = submitChurn;
window.submitAllowance = submitAllowance;
