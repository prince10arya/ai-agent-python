# AWS Database Setup Guide

## Option 1: AWS RDS PostgreSQL (Recommended)

### Advantages:
- ✅ Fully managed (automatic backups, updates, monitoring)
- ✅ High availability with Multi-AZ
- ✅ Easy scaling (vertical and horizontal)
- ✅ Free tier available (750 hours/month)
- ✅ Automated backups and point-in-time recovery

### Setup Steps:

1. **Create RDS Instance:**
   ```
   AWS Console → RDS → Create Database
   ```

2. **Configuration:**
   - Engine: PostgreSQL 15.x
   - Template: Free tier (or Production)
   - DB instance identifier: `email-agent-db`
   - Master username: `postgres`
   - Master password: [Create strong password]
   - Instance class: `db.t3.micro` (free tier)
   - Storage: 20 GB SSD
   - Public access: Yes (for development)
   - VPC security group: Create new
     - Inbound rule: PostgreSQL (5432) from your IP

3. **Get Connection Details:**
   ```
   RDS Console → Databases → email-agent-db → Connectivity & security
   ```
   - Endpoint: `email-agent-db.xxxxxx.us-east-1.rds.amazonaws.com`
   - Port: `5432`

4. **Update `.env`:**
   ```env
   AWS_RDS_ENDPOINT=email-agent-db.xxxxxx.us-east-1.rds.amazonaws.com
   AWS_RDS_USER=postgres
   AWS_RDS_PASSWORD=your-password
   AWS_RDS_DB=postgres
   
   DATABASE_URL=postgresql+psycopg://postgres:your-password@email-agent-db.xxxxxx.us-east-1.rds.amazonaws.com:5432/postgres
   ```

5. **Test Connection:**
   ```bash
   curl http://localhost:8001/api/health/detailed
   ```

### Cost Estimate:
- **Free Tier:** 750 hours/month of db.t3.micro (enough for 1 instance 24/7)
- **After Free Tier:** ~$15-20/month for db.t3.micro

---

## Option 2: AWS Aurora Serverless (Auto-scaling)

### Advantages:
- ✅ Auto-scales based on demand
- ✅ Pay only for what you use
- ✅ PostgreSQL compatible
- ✅ Scales to zero when not in use

### Setup:
```
AWS Console → RDS → Create Database
- Engine: Amazon Aurora
- Edition: PostgreSQL-compatible
- Capacity type: Serverless v2
- Min capacity: 0.5 ACU
- Max capacity: 1 ACU
```

### Cost:
- ~$0.12 per ACU-hour
- ~$0.10 per GB-month storage

---

## Option 3: AWS DynamoDB (NoSQL Alternative)

### When to Use:
- High write throughput needed
- Flexible schema
- Key-value access patterns

### Not Recommended Because:
- Your data is relational
- Need complex queries (filtering, sorting)
- SQL is simpler for email history

---

## Security Best Practices

1. **Use Secrets Manager:**
   ```bash
   aws secretsmanager create-secret \
     --name email-agent/db-password \
     --secret-string "your-password"
   ```

2. **Enable SSL:**
   ```env
   DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db?sslmode=require
   ```

3. **Restrict Security Group:**
   - Only allow your application IP
   - Use VPC for production

4. **Enable Encryption:**
   - Encryption at rest (enabled by default)
   - Encryption in transit (SSL)

---

## Connection String Format

**Standard RDS:**
```
postgresql+psycopg://USERNAME:PASSWORD@ENDPOINT:5432/DATABASE
```

**With SSL:**
```
postgresql+psycopg://USERNAME:PASSWORD@ENDPOINT:5432/DATABASE?sslmode=require
```

**Example:**
```
postgresql+psycopg://postgres:MyPass123@email-db.abc123.us-east-1.rds.amazonaws.com:5432/postgres
```

---

## Troubleshooting

**Cannot connect:**
- Check security group allows port 5432 from your IP
- Verify public accessibility is enabled
- Check VPC and subnet settings

**Timeout errors:**
- Increase connection timeout in app
- Check if RDS instance is running
- Verify network connectivity

**SSL errors:**
- Add `?sslmode=require` to connection string
- Download RDS CA certificate if needed

---

## Monitoring

**CloudWatch Metrics:**
- CPU Utilization
- Database Connections
- Free Storage Space
- Read/Write IOPS

**Enable Enhanced Monitoring:**
- RDS Console → Modify → Enable Enhanced Monitoring
- View real-time metrics

---

## Backup & Recovery

**Automated Backups:**
- Retention: 7 days (default)
- Backup window: Set preferred time

**Manual Snapshots:**
```
RDS Console → Snapshots → Take Snapshot
```

**Point-in-Time Recovery:**
- Restore to any point within retention period
