// +page.server.js
export function load() {
    const tableData = [
      { id: 45, response: 200, lines: "0 L", word: "1 W", chars: 30, payload: "sudo", length: 0.541, error: false },
      { id: 46, response: 200, lines: "0 L", word: "1 W", chars: 30, payload: "root", length: 0.526, error: false },
      { id: 47, response: 200, lines: "0 L", word: "1 W", chars: 30, payload: "guest", length: 0.468, error: false },
      { id: 48, response: 200, lines: "109 W", word: "1 W", chars: 1491, payload: "info", length: 0.552, error: false },
      { id: 49, response: 200, lines: "0 L", word: "49 W", chars: 703, payload: "test", length: 0.527, error: false },
      { id: 50, response: 200, lines: "0 L", word: "1 W", chars: 30, payload: "user", length: 0.492, error: false },
      { id: 51, response: 200, lines: "0 L", word: "1 W", chars: 30, payload: "NULL", length: 0.531, error: false },
      { id: 52, response: 200, lines: "0 L", word: "1 W", chars: 30, payload: "undefined", length: 0.533, error: false },
    ];
  
    const tableColumns = [
      { key: "id", label: "ID" },
      { key: "response", label: "Response" },
      { key: "lines", label: "Lines" },
      { key: "word", label: "Word" },
      { key: "chars", label: "Chars" },
      { key: "payload", label: "Payload" },
      { key: "length", label: "Length" },
      { key: "error", label: "Error" },
    ];
  
  
    return {
      tableData,
      tableColumns,
    };
  }