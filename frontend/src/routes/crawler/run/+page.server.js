export function load() {
  let tableData = [];

  tableData = [
    { id: 45, url: "https://juice-shop.herokuapp.com", title: "OWASP Juice Shop", wordCount: 200, charCount: 1024, linksFound: 10, error: false },
    { id: 46, url: "https://juice-shop.herokuapp.com/about", title: "About Us", wordCount: 150, charCount: 850, linksFound: 5, error: false },
    { id: 47, url: "https://juice-shop.herokuapp.com/contact", title: "Contact Us", wordCount: 100, charCount: 500, linksFound: 4, error: false },
    { id: 48, url: "https://juice-shop.herokuapp.com/login", title: "Login", wordCount: 80, charCount: 450, linksFound: 3, error: false },
    { id: 49, url: "https://juice-shop.herokuapp.com/register", title: "Register", wordCount: 75, charCount: 420, linksFound: 3, error: false },
    { id: 50, url: "https://juice-shop.herokuapp.com/products/1", title: "Apple Juice", wordCount: 120, charCount: 600, linksFound: 8, error: false },
    { id: 51, url: "https://juice-shop.herokuapp.com/products/2", title: "Orange Juice", wordCount: 115, charCount: 580, linksFound: 8, error: false },
    { id: 52, url: "https://juice-shop.herokuapp.com/faq", title: "FAQ", wordCount: 200, charCount: 1024, linksFound: 6, error: false },
    { id: 53, url: "https://juice-shop.herokuapp.com/privacy-policy", title: "Privacy Policy", wordCount: 180, charCount: 940, linksFound: 4, error: false },
    { id: 54, url: "https://juice-shop.herokuapp.com/terms-of-service", title: "Terms of Service", wordCount: 220, charCount: 1100, linksFound: 7, error: false },
    { id: 55, url: "https://juice-shop.herokuapp.com/sitemap", title: "Sitemap", wordCount: 160, charCount: 800, linksFound: 5, error: false },
    { id: 56, url: "https://juice-shop.herokuapp.com/blog", title: "Blog", wordCount: 300, charCount: 1500, linksFound: 12, error: false },
    { id: 57, url: "https://juice-shop.herokuapp.com/blog/post1", title: "Blog Post 1", wordCount: 250, charCount: 1300, linksFound: 10, error: false },
    { id: 58, url: "https://juice-shop.herokuapp.com/blog/post2", title: "Blog Post 2", wordCount: 270, charCount: 1400, linksFound: 11, error: false },
    { id: 59, url: "https://juice-shop.herokuapp.com/blog/post3", title: "Blog Post 3", wordCount: 290, charCount: 1600, linksFound: 13, error: false },
    { id: 60, url: "https://juice-shop.herokuapp.com/blog/post4", title: "Blog Post 4", wordCount: 310, charCount: 1700, linksFound: 14, error: false },
    { id: 61, url: "https://juice-shop.herokuapp.com/blog/post5", title: "Blog Post 5", wordCount: 330, charCount: 1800, linksFound: 15, error: false },
    { id: 62, url: "https://juice-shop.herokuapp.com/blog/post6", title: "Blog Post 6", wordCount: 350, charCount: 1900, linksFound: 16, error: false },
    { id: 63, url: "https://juice-shop.herokuapp.com/blog/post7", title: "Blog Post 7", wordCount: 370, charCount: 2000, linksFound: 17, error: false },
    { id: 64, url: "https://juice-shop.herokuapp.com/blog/post8", title: "Blog Post 8", wordCount: 390, charCount: 2100, linksFound: 18, error: false },
    { id: 65, url: "https://juice-shop.herokuapp.com/blog/post9", title: "Blog Post 9", wordCount: 410, charCount: 2200, linksFound: 19, error: false },
    { id: 66, url: "https://juice-shop.herokuapp.com/blog/post10", title: "Blog Post 10", wordCount: 430, charCount: 2300, linksFound: 20, error: false },
    ];

  const tableColumns = [
    { key: "id", label: "ID" },
    { key: "url", label: "URL", isLink: true },
    { key: "title", label: "Title" },
    { key: "wordCount", label: "Word Count" },
    { key: "charCount", label: "Character Count" },
    { key: "linksFound", label: "Links Found" },
    { key: "error", label: "Error" },
  ];

  return {
    tableData,
    tableColumns,
  };
}