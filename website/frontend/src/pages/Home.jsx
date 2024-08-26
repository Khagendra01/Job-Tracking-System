import { useState, useEffect } from "react";
import api from "../api";
import Job from "../components/Job"
import "../styles/Home.css"

function Home() {
    const [jobs, setJobs] = useState([]);
    const [title, setTitle] = useState("");
    const [status, setStatus] = useState("");
    const [company, setCompany] = useState("");

    useEffect(() => {
        getJobs();
    }, []);

    const getJobs = () => {
        api
            .get("/api/jobs/")
            .then((res) => res.data)
            .then((data) => {
                setJobs(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const deleteJob = (id) => {
        api
            .delete(`/api/jobs/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Job deleted!");
                else alert("Failed to Job job.");
                getJobs();
            })
            .catch((error) => alert(error));
    };

    const createJob = (e) => {
        e.preventDefault();
        api
            .post("/api/jobs/", { title, status, company })
            .then((res) => {
                if (res.status === 201) alert("job created!");
                else alert("Failed to make job.");
                getJobs();
            })
            .catch((err) => alert(err));
    };

    return (
        <div>
            <div>
                <h2>Job Listings</h2>
                {jobs.map((job) => (
                    <Job job={job} onDelete={deleteJob} key={job.id} />
                ))}
            </div>
            <h2>Create a job</h2>
            <form onSubmit={createJob}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="status">Status:</label>
                <br />
                <input
                    type="text"
                    id="status"
                    name="status"
                    required
                    onChange={(e) => setStatus(e.target.value)}
                    value={status}
                />
                <label htmlFor="company">Company:</label>
                <br />
                <input
                    type="text"
                    id="company"
                    name="company"
                    required
                    onChange={(e) => setCompany(e.target.value)}
                    value={company}
                />
                <br />

                <input type="submit" value="Submit"></input>
            </form>
        </div>
    );
}

export default Home;