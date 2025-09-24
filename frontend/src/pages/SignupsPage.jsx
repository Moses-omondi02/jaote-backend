import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

import SignupForm from "./_SignupForm";

/* simple view to enter signup for a task id (mock) */
export default function SignupsPage() {
  // we show a small UI to allow signup with task id (since backend not ready)
  return (
    <div className="container">
      <h2>Sign Up for a Task</h2>
      <p className="muted">Enter your details and the task ID you want to sign up for.</p>
      <SignupForm taskId={null} onDone={() => { /* optional callback */ }} />
    </div>
  );
}
