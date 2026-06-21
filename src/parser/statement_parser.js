// statement_parser.js – parses uploaded statements

// Configure PDF.js worker to avoid main-thread parsing
if (typeof window !== 'undefined' && window.pdfjsLib) {
  window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
}
/**
 * Parse a statement file (CSV or PDF) and return a JSON string of transactions.
 * For CSV files the columns are expected to include: date, description, amount.
 * PDF parsing is not implemented yet – see TODO below.
 *
 * @param {File} file - The File object from an input element.
 * @returns {Promise<string>} - Resolves to a JSON string representing an array of transaction objects.
 */
export async function parseStatement(file) {
  try {
    const text = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(reader.error);
      reader.readAsText(file);
    });

    // Simple MIME‑type/extension check for CSV
    const isCsv = file.type === 'text/csv' || file.name.toLowerCase().endsWith('.csv');
    if (isCsv) {
      // Split into rows, trim empty lines
      const rows = text.split(/\r?\n/).filter((r) => r.trim() !== '');
      if (rows.length === 0) return JSON.stringify([]);

      // Assume first row is header
      const rawHeader = rows[0].split(',');
      const headerMap = {};
      rawHeader.forEach((h, idx) => {
        const normalized = h.replace(/[\uFEFF\u200B\u200C\u200D\ufeff"']+|[\uFEFF\u200B\u200C\u200D\ufeff"']+$/g, '').trim().toLowerCase();
        headerMap[normalized] = idx;
      });
      const dateIdx = headerMap['date'];
      const descIdx = headerMap['description'];
      const amountIdx = headerMap['amount'];

      const transactions = rows.slice(1).map((row) => {
        const cols = row.split(',').map(c => c.replace(/^['"\r]+|['"\r]+$/g, '').trim());
        return {
          date: dateIdx >= 0 ? cols[dateIdx] : null,
          description: descIdx >= 0 ? cols[descIdx] : null,
          amount: amountIdx >= 0 ? parseFloat(cols[amountIdx]) : null,
        };
      });
      return JSON.stringify(transactions);
    }

    // PDF parsing using pdfjsLib
if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
  // Read the file as an ArrayBuffer
  const arrayBuffer = await new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(reader.error);
    reader.readAsArrayBuffer(file);
  });

  // Load PDF document
  const pdfDoc = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  const numPages = pdfDoc.numPages;
  let fullText = '';
  for (let i = 1; i <= numPages; i++) {
    const page = await pdfDoc.getPage(i);
    const textContent = await page.getTextContent();
    const pageText = textContent.items.map(item => item.str).join(' ');
    fullText += ' ' + pageText;
  }

  // Extract transactions using regex: date - description - $amount
  const regex = /(\d{2}\/\d{2}\/\d{4})\s*-\s*(.*?)\s*-\s*\$([\d.]+)/g;
  const matches = [];
  let match;
  while ((match = regex.exec(fullText)) !== null) {
    const [_, date, description, amountStr] = match;
    matches.push({
      date: date,
      description: description.trim(),
      amount: parseFloat(amountStr)
    });
  }
  return JSON.stringify(matches);
}
    throw new Error('Unsupported file type for parsing');
  } catch (err) {
    console.error('Error parsing statement:', err);
    throw err;
  }
}
