document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('queryForm');
  const sqlQueryOutput = document.getElementById('sqlQueryOutput'); // ✅ FIXED ID
  const queryResultOutput = document.getElementById('queryResultOutput');
  const copyQueryBtn = document.getElementById('copyQueryBtn');
  const toast = document.getElementById('toast');

  function showToast(message, isError = false) {
    toast.textContent = message;
    toast.classList.remove('hidden');
    toast.classList.toggle('bg-green-500', !isError);
    toast.classList.toggle('bg-red-500', isError);
    setTimeout(() => toast.classList.add('hidden'), 3000);
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const dbName = document.getElementById('dbName').value.trim();
    const question = document.getElementById('question').value.trim();

    if (!dbName || !question) {
      showToast('Please enter both database name and question.', true);
      return;
    }

    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ db_name: dbName, question }),
      });

      const data = await res.json();
      console.log("Response from backend:", data);

      if (res.ok) {
        sqlQueryOutput.textContent = data.sql || 'No query generated.';

        // Display result as table
        if (Array.isArray(data.result) && data.result.length > 0) {
          const headers = Object.keys(data.result[0]);
          const table = document.createElement('table');
          table.classList.add('min-w-full', 'bg-white', 'border', 'border-gray-200', 'text-sm');

          const thead = document.createElement('thead');
          const headerRow = document.createElement('tr');
          headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            th.classList.add('border', 'px-4', 'py-2', 'bg-gray-100');
            headerRow.appendChild(th);
          });
          thead.appendChild(headerRow);
          table.appendChild(thead);

          const tbody = document.createElement('tbody');
          data.result.forEach(row => {
            const tr = document.createElement('tr');
            headers.forEach(header => {
              const td = document.createElement('td');
              td.textContent = row[header];
              td.classList.add('border', 'px-4', 'py-2');
              tr.appendChild(td);
            });
            tbody.appendChild(tr);
          });
          table.appendChild(tbody);

          queryResultOutput.innerHTML = '';
          queryResultOutput.appendChild(table);
        } else {
          queryResultOutput.innerHTML = '<p>No results found.</p>';
        }
      } else {
        showToast(data.error || 'Something went wrong.', true);
      }
    } catch (err) {
      console.error("Fetch error:", err);
      showToast('Failed to connect to backend.', true);
    }
  });

  copyQueryBtn.addEventListener('click', () => {
    const text = sqlQueryOutput.textContent;
    if (text.trim()) {
      navigator.clipboard.writeText(text).then(() => {
        showToast('Query copied to clipboard!');
      });
    } else {
      showToast('Nothing to copy.', true);
    }
  });
});
