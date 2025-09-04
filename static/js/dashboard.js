// dashboard.js

document.addEventListener("DOMContentLoaded", () => {
  // Select all cards with the 'data-url' attribute
  const cards = document.querySelectorAll(".card[data-url]");

  cards.forEach(card => {
      const url = card.getAttribute("data-url");

      // Fetch data from the URL
      fetch(url)
          .then(response => response.json())
          .then(data => {
              // Customize this to suit the structure of each data file
              const descriptionElement = card.querySelector(".card-description");
              let content = "";

              if (data.type === "inspections") {
                  content = `
                      <p>Inspections Passed: ${data.inspections_passed}</p>
                      <p>Upcoming Inspections: ${data.upcoming_inspections}</p>
                  `;
              } else if (data.type === "feedback") {
                  content = `
                      <p>Positive Feedback: ${data.positive}</p>
                      <p>Negative Feedback: ${data.negative}</p>
                  `;
              } else if (data.type === "poisoning_cases") {
                  content = `
                      <p>Reported Cases: ${data.reported_cases}</p>
                      <p>Resolved Cases: ${data.resolved_cases}</p>
                  `;
              } else {
                  content = "<p>Data unavailable</p>";
              }

              // Update card content
              descriptionElement.innerHTML = content;
          })
          .catch(error => {
              console.error("Error fetching data:", error);
              card.querySelector(".card-description").textContent = "Error loading data.";
          });
  });
});
