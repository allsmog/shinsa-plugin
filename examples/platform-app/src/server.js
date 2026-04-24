export function health() {
  return { status: "ok", checkedAt: new Date().toISOString() };
}

export function validateInput(value) {
  if (typeof value !== "string" || value.length > 120) {
    throw new Error("invalid input");
  }
  return value.trim();
}
