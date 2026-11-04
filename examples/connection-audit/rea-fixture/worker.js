// A static endpoint candidate, not evidence that a network request occurred.
exports.send = async function send(payload) {
  return fetch('https://example.invalid/events', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
};
