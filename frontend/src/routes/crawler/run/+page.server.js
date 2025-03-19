export function load() {
  const tableData = [
    { id: 45, url: "https://juice-shop.herokuapp.com", title: "OWASP Juice Shop", wordCount: 200, charCount: 1024, linksFound: 10, error: false },
    { id: 46, url: "https://juice-shop.herokuapp.com/about", title: "About Us", wordCount: 150, charCount: 850, linksFound: 5, error: false },
    { id: 47, url: "https://juice-shop.herokuapp.com/contact", title: "Contact Us", wordCount: 100, charCount: 500, linksFound: 4, error: false },
    { id: 48, url: "https://juice-shop.herokuapp.com/login", title: "Login", wordCount: 80, charCount: 450, linksFound: 3, error: false },
    { id: 49, url: "https://juice-shop.herokuapp.com/register", title: "Register", wordCount: 75, charCount: 420, linksFound: 3, error: false },
    { id: 50, url: "https://juice-shop.herokuapp.com/products/1", title: "Apple Juice", wordCount: 120, charCount: 600, linksFound: 8, error: false },
    { id: 51, url: "https://juice-shop.herokuapp.com/products/2", title: "Orange Juice", wordCount: 115, charCount: 580, linksFound: 8, error: false },
    { id: 52, url: "https://juice-shop.herokuapp.com/faq", title: "FAQ", wordCount: 200, charCount: 1024, linksFound: 6, error: false },
    { id: 53, url: "https://juice-shop.herokuapp.com/privacy-policy", title: "Privacy Policy", wordCount: 180, charCount: 940, linksFound: 4, error: false },
  ];

  return {
    tableData
  };
}
