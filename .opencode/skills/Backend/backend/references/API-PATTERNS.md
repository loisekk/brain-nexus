# TypeScript Backend Patterns

> Type-safe API development patterns

## Repository Pattern

```typescript
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, 'id'>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
}

class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    return await db.users.findUnique({ where: { id } });
  }
  // ... other methods
}
```

## Service Layer

```typescript
class UserService {
  constructor(private repo: Repository<User>) {}

  async createUser(input: CreateUserInput): Promise<User> {
    const existing = await this.repo.findByEmail(input.email);
    if (existing) throw new ConflictError('Email exists');
    return this.repo.create(input);
  }
}
```

## Response Types

```typescript
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function success<T>(data: T): ApiResponse<T> {
  return { success: true, data };
}

function error(message: string): ApiResponse<never> {
  return { success: false, error: message };
}
```

## Middleware Types

```typescript
type Middleware = (
  req: Request,
  res: Response,
  next: NextFunction
) => Promise<void> | void;

const authMiddleware: Middleware = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  req.user = await verifyToken(token);
  next();
};
```

---

**Author:** Dr. Umit Kacar & Muhsin Elcicek
