// export async function POST({ request }) {
// console.log("POST handler in +server.js triggered");

//   try {
//       const formData = await request.json();
//       console.log("Received data in SvelteKit server:", formData);

//         // Transform data to match backend expectations
//         const transformedData = {
//         target_url: formData["target-url"],
//         depth: formData["depth"] ? Number(formData["depth"]) : undefined,
//         max_pages: formData["max-pages"] ? Number(formData["max-pages"]) : undefined,
//         user_agent: formData["user-agent"],
//         delay: formData["delay"] ? Number(formData["delay"]) : undefined,
//         proxy: formData["proxy"] ? Number(formData["proxy"]) : undefined
//         };

//         console.log("Transformed data for backend:", transformedData);
    
//       // Send data to FastAPI backend
//       const backendUrl = "http://127.0.0.1:8000/api/crawler";
//       console.log(`Sending data to backend at: ${backendUrl}`);

//       const response = await fetch(backendUrl, {
//           method: "POST",
//           headers: { 
//             "Content-Type": "application/json",
//             "Accept": "application/json",
//           },
//           body: JSON.stringify(formData),
//       });

//       console.log("Backend response status:", response.status);

//       if (!response.ok) {
//         console.error("Error response from backend:", response.statusText);
//         return new Response(
//             JSON.stringify({
//                 mesage: `Backend error: ${response.statusText}`,
//                 status: response.status,
//             }),
//             {
//                 status: response.status,
//                 headers: { "Content-Type": "application/json" },
//             }
//         );
//       }

//       const result = await response.json();
//       console.log("Response from backend:", result);

//       return new Response(
//         JSON.stringify(result), 
//         {
//           status: 200,
//           headers: { "Content-Type": "application/json" },
//         }
//       );

//   } catch (error) {
//       console.error("Error processing request:", error);

//       return new Response(
//         JSON.stringify({ 
//             message: "Internal server error",
//             error: error.message,
//         }), 
//         {
//           status: 500,
//           headers: { "Content-Type": "application/json" },
//       });
//   }
// }
