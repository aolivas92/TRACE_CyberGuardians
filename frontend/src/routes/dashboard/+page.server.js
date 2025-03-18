export function load() {
  return {
      projectName: "Project 1",
      tools: [
          { name: "Crawler", status: "Not Started", route: "/crawler/config" },
          { name: "Fuzzer", status: "Started", route: "/dashboard" },
      ],
  };
}
