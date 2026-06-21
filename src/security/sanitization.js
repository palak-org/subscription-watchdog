// Sanitization and file validation utilities

/**
 * Validate file size (<5MB) and allowed extensions (.csv, .pdf).
 * @param {File} file - The file object from an input element.
 * @returns {boolean} True if the file meets criteria, otherwise false.
 */
export function validateFileStructure(file) {
  const maxSize = 5 * 1024 * 1024; // 5MB in bytes
  if (file.size > maxSize) {
    return false;
  }
  const allowedExt = ['csv', 'pdf'];
  const ext = file.name.split('.').pop().toLowerCase();
  return allowedExt.includes(ext);
}

/**
 * Basic text sanitization to prevent XSS.
 * Strips <script> tags, any HTML tags, and escapes special characters.
 * @param {string} text - Raw user-provided text.
 * @returns {string} Sanitized text safe for insertion into the DOM.
 */
export function sanitizeText(text) {
  if (typeof text !== 'string') return '';
  // Remove script tags and their content
  let sanitized = text.replace(/<script[^>]*>([\s\S]*?)<\/script>/gi, '');
  // Remove any remaining HTML tags
  sanitized = sanitized.replace(/<[^>]+>/g, '');
  // Escape special characters that could be interpreted as HTML entities
  sanitized = sanitized.replace(/[&<>'"`]/g, function (char) {
    return `\\${char}`;
  });
  return sanitized;
}

/**
 * Placeholder for deeper MIME type verification.
 * In a real application this would involve server‑side checks or
 * using a library to inspect the file's binary header.
 * @param {File} file - The file to verify.
 * @returns {boolean} Currently always true (to be implemented).
 */
export function validateMimeType(file) {
  // Basic frontend MIME type check
  const validTypes = ['text/csv', 'application/pdf'];

  if (!validTypes.includes(file.type)) {
    console.error("Security Alert: Invalid MIME type detected.");
    return false;
  }
  return true;
}
