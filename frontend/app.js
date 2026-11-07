 const API_URL = "http://127.0.0.1:8000";

// REGISTER FORM
const registerForm = document.getElementById("register-form");

if (registerForm) {
    registerForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(API_URL + "/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Registration failed");
            }

            alert("Registration successful! Please login.");
            window.location.href = "login.html";

        } catch (error) {
            alert(error.message);
        }
    });
}


// LOGIN FORM
const loginForm = document.getElementById("login-form");

if (loginForm) {
    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(API_URL + "/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Login failed");
            }

            localStorage.setItem("access_token", data.access_token);

            alert("Login successful!");
            window.location.href = "dashboard.html";

        } catch (error) {
            alert(error.message);
        }
    });
}


// DISPLAY JOBS
const jobList = document.getElementById("job-list");

if (jobList) {
    async function loadJobs() {
        try {
            const response = await fetch(API_URL + "/jobs/");
            const jobs = await response.json();

            if (!response.ok) {
                throw new Error("Failed to load jobs");
            }

            jobList.innerHTML = "";

            jobs.forEach(function(job) {
                const jobCard = document.createElement("div");
                jobCard.className = "job-card";

                const title = document.createElement("h3");
                title.textContent = job.title;

                const company = document.createElement("p");
                company.textContent = "Company: " + job.company;

                const location = document.createElement("p");
                location.textContent = "Location: " + job.location;

                const salary = document.createElement("p");
                salary.textContent = "Salary: " + (job.salary || "Not specified");

                // APPLY BUTTON
                const applyButton = document.createElement("button");
                applyButton.textContent = "Apply Now";
                applyButton.className = "btn";

                applyButton.addEventListener("click", async function() {
                    const token = localStorage.getItem("access_token");

                    if (!token) {
                        alert("Please login first to apply for jobs.");
                        window.location.href = "login.html";
                        return;
                    }

                    try {
                        const applicationResponse = await fetch(
                            API_URL + "/applications/",
                            {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                    "Authorization": "Bearer " + token
                                },
                                body: JSON.stringify({
                                    job_id: job.id,
                                    resume: "My resume"
                                })
                            }
                        );

                        const applicationData = await applicationResponse.json();

                        if (!applicationResponse.ok) {
                            throw new Error(
                                applicationData.detail || "Application failed"
                            );
                        }

                        alert("Application submitted successfully!");

                    } catch (error) {
                        alert(error.message);
                    }
                });

                // ADD JOB CARD
                jobCard.append(
                    title,
                    company,
                    location,
                    salary,
                    applyButton
                );

                jobList.appendChild(jobCard);
            });

        } catch (error) {
            jobList.textContent = error.message;
        }
    }

    loadJobs();
}
// MY APPLICATIONS
const myApplications = document.getElementById("my-applications");

if (myApplications) {
    async function loadMyApplications() {
        const token = localStorage.getItem("access_token");

        if (!token) {
            myApplications.textContent = "Please login to view your applications.";
            return;
        }

        try {
            const response = await fetch(API_URL + "/applications/my", {
                headers: {
                    "Authorization": "Bearer " + token
                }
            });

            const applications = await response.json();

            if (!response.ok) {
                throw new Error(
                    applications.detail || "Failed to load applications"
                );
            }

            myApplications.innerHTML = "";

            if (applications.length === 0) {
                myApplications.textContent = "You have not applied for any jobs yet.";
                return;
            }

            applications.forEach(function(application) {
                const card = document.createElement("div");
                card.className = "job-card";

                const jobId = document.createElement("p");
                jobId.textContent = "Job ID: " + application.job_id;

                const status = document.createElement("p");
                status.textContent = "Status: " + application.status;

                const resume = document.createElement("p");
                resume.textContent = "Resume: " + application.resume;

                card.append(jobId, status, resume);
                myApplications.appendChild(card);
            });

        } catch (error) {
            myApplications.textContent = error.message;
        }
    }

    loadMyApplications();
}
// LOGOUT
const logoutLink = document.getElementById("logout-link");

if (logoutLink) {
    logoutLink.addEventListener("click", function(event) {
        event.preventDefault();

        localStorage.removeItem("access_token");

        window.location.href = "login.html";
    });
}