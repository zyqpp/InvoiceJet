import { AbstractControl, ValidationErrors } from "@angular/forms";

// Custom validator function
export function dueDateValidator(
  control: AbstractControl
): ValidationErrors | null {
  const issueDate = control?.parent?.get("issueDate")?.value;
  const dueDate = control.value;

  if (issueDate && dueDate && new Date(dueDate) < new Date(issueDate)) {
    return { dueDateBeforeIssueDate: true };
  }
  return null;
}
