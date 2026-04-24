import bcrypt from "bcrypt";

export async function verifyPassword(candidate: string, passwordHash: string): Promise<boolean> {
  return bcrypt.compare(candidate, passwordHash);
}
