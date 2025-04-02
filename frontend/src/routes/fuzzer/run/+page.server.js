// +page.server.js
export function load() {
    const tableData = [
        {
          id: 45,
          response: 200,
          url: "http://example.com",
          payload: "sudo",
          length: 130,
          snippet: "This is a response snippet for sudo...",
          error: false,
        },
        {
          id: 46,
          response: 200,
          url: "http://example.com",
          payload: "root",
          length: 126,
          snippet: "This is a response snippet for root...",
          error: false,
        },
        {
          id: 47,
          response: 200,
          url: "http://example.com",
          payload: "guest",
          length: 115,
          snippet: "This is a response snippet for guest...",
          error: false,
        },
        {
          id: 48,
          response: 200,
          url: "http://example.com",
          payload: "info",
          length: 1491,
          snippet: "Response content starting with info...",
          error: false,
        },
        {
          id: 49,
          response: 403,
          url: "http://example.com",
          payload: "test",
          length: 703,
          snippet: "403 forbidden content...",
          error: true,
        },
        {
          id: 50,
          response: 200,
          url: "http://example.com",
          payload: "user",
          length: 132,
          snippet: "Data for user payload...",
          error: false,
        },
        {
          id: 51,
          response: 500,
          url: "http://example.com",
          payload: "NULL",
          length: 165,
          snippet: "Internal server error maybe...",
          error: true,
        },
        {
          id: 52,
          response: 200,
          url: "http://example.com",
          payload: "undefined",
          length: 133,
          snippet: "Payload undefined result...",
          error: false,
        },
      ];
  
    const tableColumns = [
        { key: "id", label: "ID" },
        { key: "response", label: "Response" },
        { key: "url", label: "URL" },
        { key: "payload", label: "Payload" },
        { key: "length", label: "Length (chars)" },
        { key: "snippet", label: "Snippet" },
        { key: "error", label: "Error" },
      ];
  
  
    return {
      tableData,
      tableColumns,
    };
  }