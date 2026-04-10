const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  if (!resumeFile || !jobTitle || !jobDescription) return;

  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_title", jobTitle);
  formData.append("job_description", jobDescription);

  const response = await fetch("http://127.0.0.1:8000/process_resume/", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  console.log(data); // This will show the backend response
  alert(data.message);
};