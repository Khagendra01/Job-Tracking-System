import React from "react";
import "../styles/Job.css"

function Job({ job, onDelete }) {
    const formattedDate = new Date(job.created_at).toLocaleDateString("en-US")

    return (
        <div className="job-container">
            <div className="job-header">
                <span className="header-item">Title</span>
                <span className="header-item">Status</span>
                <span className="header-item">Company</span>
                <span className="header-item">Date Applied</span>
                <span className="header-item">Action</span>
            </div>
            <div className="job-details">
                <p className="job-title">{job.title}</p>
                <p className="job-content">{job.status}</p>
                <p className="job-content">{job.company}</p>
                <p className="job-date">{formattedDate}</p>
                <button className="delete-button" onClick={() => onDelete(job.id)}>
                    Delete
                </button>
            </div>
        </div>
    );
}

export default Job