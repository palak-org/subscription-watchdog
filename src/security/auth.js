// Simple authentication utilities for local testing

/**
 * Mock login – stores a dummy token in sessionStorage.
 * @param {string} username
 * @param {string} password
 */
export function login(username, password) {
  // In real app, you'd verify credentials with a server.
  const dummyToken = btoa(`${username}:${password}`); // simple base64 token
  sessionStorage.setItem('authToken', dummyToken);
  console.log(`User "${username}" logged in (mock)`);
}

/**
 * Verify access – checks for authToken in sessionStorage.
 * @returns {boolean} true if token exists, false otherwise.
 */
export function verifyUserAccess() {
  const token = sessionStorage.getItem('authToken');
  if (!token) {
    console.warn('Security Error: Unauthorized access');
    return false;
  }
  return true;
}

/**
 * Logout – removes authToken from sessionStorage.
 */
export function logout() {
  sessionStorage.removeItem('authToken');
  console.log('User logged out (mock)');
}

