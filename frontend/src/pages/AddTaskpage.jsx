import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const schema = Yup.object({
  title: Yup.string().required("Title required"),
  description: Yup.string().required("Description required"),
  hours: Yup.number().typeError("Hours must be a number").min(0, "Min 0").required("Hours required"),
  location: Yup.string().required("Location required"),
  date: Yup.string().matches(/^\d{4}-\d{2}-\d{2}$/, "Use YYYY-MM-DD").required("Date required"),
});

export default function AddTaskPage() {
  return (
    <div className="container">
      <h2>Post a New Task</h2>
      <Formik
        initialValues={{ title: "", description: "", hours: "", location: "", date: "" }}
        validationSchema={schema}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          // replace with POST fetch to backend /tasks
          console.log("CREATE TASK (mock)", values);
          setTimeout(()=> {
            setSubmitting(false);
            resetForm();
            alert("Task created (mock) — backend not connected yet.");
          }, 600);
        }}
      >
        {({ isSubmitting }) => (
          <Form className="form-card">
            <label>Title</label>
            <Field name="title" />
            <ErrorMessage name="title" component="div" className="error" />

            <label>Description</label>
            <Field as="textarea" name="description" rows="4" />
            <ErrorMessage name="description" component="div" className="error" />

            <label>Hours Required</label>
            <Field name="hours" />
            <ErrorMessage name="hours" component="div" className="error" />

            <label>Location</label>
            <Field name="location" />
            <ErrorMessage name="location" component="div" className="error" />

            <label>Date (YYYY-MM-DD)</label>
            <Field name="date" placeholder="2025-10-01" />
            <ErrorMessage name="date" component="div" className="error" />

            <div style={{marginTop:12}}>
              <button className="btn primary" type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Posting..." : "Post Task"}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}
