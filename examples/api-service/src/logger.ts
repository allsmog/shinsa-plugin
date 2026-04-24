export const logger = {
  warn(message: string, fields: Record<string, unknown>): void {
    console.warn(message, redact(fields));
  },
};

function redact(fields: Record<string, unknown>): Record<string, unknown> {
  const copy = { ...fields };
  delete copy.authorization;
  return copy;
}
