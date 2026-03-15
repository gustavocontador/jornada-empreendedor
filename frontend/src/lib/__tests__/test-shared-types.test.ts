import { testSharedTypes } from '../test-shared-types';

describe('testSharedTypes', () => {
  it('should create valid user and assessment objects', () => {
    const { user, assessment } = testSharedTypes();

    // Validate user structure
    expect(user).toHaveProperty('id');
    expect(user).toHaveProperty('email');
    expect(user).toHaveProperty('full_name');
    expect(user).toHaveProperty('role');
    expect(user.role).toBe('user');

    // Validate assessment structure
    expect(assessment).toHaveProperty('id');
    expect(assessment).toHaveProperty('user_id');
    expect(assessment).toHaveProperty('status');
    expect(assessment).toHaveProperty('scores');
    expect(assessment.status).toBe('draft');
    expect(assessment.user_id).toBe(user.id);
  });

  it('should have correct types from shared workspace', () => {
    const { user, assessment } = testSharedTypes();

    expect(typeof user.id).toBe('string');
    expect(typeof user.email).toBe('string');
    expect(typeof user.full_name).toBe('string');
    expect(['user', 'admin', 'specialist']).toContain(user.role);

    expect(typeof assessment.id).toBe('string');
    expect(typeof assessment.user_id).toBe('string');
    expect(['draft', 'completed']).toContain(assessment.status);
    expect(typeof assessment.scores).toBe('object');
  });
});
