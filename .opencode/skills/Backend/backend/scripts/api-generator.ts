#!/usr/bin/env npx ts-node

/**
 * TypeScript API Route Generator
 * Generates type-safe API endpoints
 *
 * @author Dr. Umit Kacar & Muhsin Elcicek
 * @version 1.0.0
 */

interface EntityField {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'Date';
  required: boolean;
}

interface EntityConfig {
  name: string;
  fields: EntityField[];
}

function generateTypes(entity: EntityConfig): string {
  const { name, fields } = entity;

  const fieldDefs = fields
    .map(f => `  ${f.name}${f.required ? '' : '?'}: ${f.type};`)
    .join('\n');

  return `
// ${name} Types
interface ${name} {
  id: string;
${fieldDefs}
  createdAt: Date;
  updatedAt: Date;
}

type Create${name}Input = Omit<${name}, 'id' | 'createdAt' | 'updatedAt'>;
type Update${name}Input = Partial<Create${name}Input>;

interface ${name}Response {
  data: ${name};
  message?: string;
}

interface ${name}ListResponse {
  data: ${name}[];
  total: number;
  page: number;
  pageSize: number;
}
`.trim();
}

function generateController(entity: EntityConfig): string {
  const { name } = entity;
  const nameLower = name.toLowerCase();

  return `
// ${name} Controller
import { Request, Response } from 'express';
import { ${name}Service } from './${nameLower}.service';

export class ${name}Controller {
  constructor(private service: ${name}Service) {}

  async getAll(req: Request, res: Response): Promise<void> {
    const { page = 1, pageSize = 10 } = req.query;
    const result = await this.service.findAll({ page: +page, pageSize: +pageSize });
    res.json(result);
  }

  async getById(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const result = await this.service.findById(id);
    if (!result) {
      res.status(404).json({ message: '${name} not found' });
      return;
    }
    res.json({ data: result });
  }

  async create(req: Request, res: Response): Promise<void> {
    const result = await this.service.create(req.body);
    res.status(201).json({ data: result });
  }

  async update(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const result = await this.service.update(id, req.body);
    res.json({ data: result });
  }

  async delete(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    await this.service.delete(id);
    res.status(204).send();
  }
}
`.trim();
}

// Example usage
const exampleEntity: EntityConfig = {
  name: 'User',
  fields: [
    { name: 'email', type: 'string', required: true },
    { name: 'name', type: 'string', required: true },
    { name: 'age', type: 'number', required: false }
  ]
};

console.log('Generated Types:\n');
console.log(generateTypes(exampleEntity));
console.log('\n' + '='.repeat(50) + '\n');
console.log('Generated Controller:\n');
console.log(generateController(exampleEntity));

export { generateTypes, generateController, EntityConfig };
