document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('expense-form');
  const messageDiv = document.getElementById('message');
  const expensesList = document.getElementById('expenses-list');
  const importForm = document.getElementById('import-form');
  const importMessageDiv = document.getElementById('import-message');

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    
    fetch('/expenses', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      messageDiv.textContent = data.message;
      form.reset();
      
      // Refresh the expenses list
      refreshExpensesList();
    })
    .catch(error => {
      console.error('Error:', error);
      messageDiv.textContent = 'An error occurred. Please try again.';
    });
  });

  importForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(importForm);
    
    fetch('/import-statement', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      importMessageDiv.textContent = data.message;
      importForm.reset();
      
      // Refresh the expenses list
      refreshExpensesList();
    })
    .catch(error => {
      console.error('Error:', error);
      importMessageDiv.textContent = 'An error occurred during import. Please try again.';
    });
  });

  function refreshExpensesList() {
    fetch('/expenses')
      .then(response => response.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newExpensesList = doc.getElementById('expenses-list');
        expensesList.innerHTML = newExpensesList.innerHTML;
      });
  }

  // Set the default date to today
  const dateInput = document.getElementById('date');
  const today = new Date().toISOString().split('T')[0];
  dateInput.value = today;
});