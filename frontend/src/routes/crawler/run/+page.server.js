export async function load({ params, url, fetch }) {
  let tableData = [];
  let jobId = url.searchParams.get('jobId');

  console.log('🔍 Loading crawler run page with job ID:', jobId);

  // Define the table columns structure
  const tableColumns = [
    { key: "id", label: "ID" },
    { key: "url", label: "URL", isLink: true },
    { key: "title", label: "Title" },
    { key: "wordCount", label: "Word Count" },
    { key: "charCount", label: "Character Count" },
    { key: "linksFound", label: "Links Found" },
    { key: "error", label: "Error" },
  ];

  // If we have a job ID, try to fetch real data
  if (jobId) {
    console.log('🔄 Fetching results from backend for job:', jobId);
    
    try {
      // Fetch job status first
      const statusResponse = await fetch(`http://127.0.0.1:8000/api/crawler/${jobId}`);
      
      if (statusResponse.ok) {
        const statusData = await statusResponse.json();
        console.log('ℹ️ Job status:', statusData.status, `(Progress: ${statusData.progress}%)`);
      }
      
      // Then fetch results
      const response = await fetch(`http://127.0.0.1:8000/api/crawler/${jobId}/results`);
      
      if (response.ok) {
        const data = await response.json();
        console.log('📊 Received results from backend with', data.results?.length || 0, 'items');
        
        if (data && data.results && Array.isArray(data.results)) {
          // Transform the backend data to match our table format
          tableData = data.results.map((item, index) => ({
            id: index + 1,
            url: item.url,
            title: item.title || 'No Title',
            wordCount: item.wordCount || item.word_count || 0,
            charCount: item.charCount || item.char_count || 0,
            linksFound: item.linksFound || item.links_found || 0,
            error: item.error || false
          }));
          
          console.log('✅ Successfully processed', tableData.length, 'result items');
        } else {
          console.warn('⚠️ Received empty or invalid results data');
        }
      } else {
        console.warn('⚠️ Backend response not OK:', response.status, response.statusText);
      }
      
      // Get logs too
      try {
        const logsResponse = await fetch(`http://127.0.0.1:8000/api/crawler/${jobId}/logs`);
        if (logsResponse.ok) {
          const logsData = await logsResponse.json();
          console.log('📝 Received', logsData.logs?.length || 0, 'log entries');
        }
      } catch (logsError) {
        console.error('❌ Error fetching logs:', logsError);
      }
      
    } catch (error) {
      console.error('🔥 Error fetching crawler results:', error);
    }
  } else {
    console.log('ℹ️ No job ID provided, will use mock data');
    // Use mock data if we couldn't get real data
    if (tableData.length === 0) {
      console.log('🧪 Using mock data for display');
      tableData = [
        { id: 45, url: "https://juice-shop.herokuapp.com", title: "OWASP Juice Shop", wordCount: 200, charCount: 1024, linksFound: 10, error: false },
        { id: 46, url: "https://juice-shop.herokuapp.com/about", title: "About Us", wordCount: 150, charCount: 850, linksFound: 5, error: false },
        // ... more mock data entries ...
      ];
    }
  }


  console.log('🚀 Crawler run page loaded with', tableData.length, 'results');
  
  return {
    tableData,
    tableColumns,
    jobId
  };
}