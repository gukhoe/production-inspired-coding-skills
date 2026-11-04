// Synthetic source-analysis fixture; REA inspects this without executing it.
const worker = require('./worker');
exports.submit = async function submit(payload) {
  return worker.send(payload);
};
