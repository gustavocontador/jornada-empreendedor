export interface UserSchema {
  id: string;
  email: string;
  full_name: string;
  role: 'user' | 'admin' | 'specialist';
}
