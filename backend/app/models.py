from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cluster(db.Model):
    __tablename__ = "clusters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    api_server = db.Column(db.Text, nullable=False)
    kubeconfig = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship("User", backref=db.backref("clusters", lazy=True))

class Namespace(db.Model):
    __tablename__ = "namespaces"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey("clusters.id", ondelete="CASCADE"), nullable=False)
    last_synced_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("name", "cluster_id", name="_namespace_cluster_uc"),)

    cluster = db.relationship("Cluster", backref=db.backref("namespaces", lazy=True))

class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(50), nullable=False)
    namespace_id = db.Column(db.Integer, db.ForeignKey("namespaces.id", ondelete="CASCADE"))
    cluster_id = db.Column(db.Integer, db.ForeignKey("clusters.id", ondelete="CASCADE"))
    labels = db.Column(db.JSON)
    spec = db.Column(db.JSON)
    status = db.Column(db.JSON)
    last_synced_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("name", "kind", "namespace_id", "cluster_id", name="_resource_uc"),)

    namespace = db.relationship("Namespace", backref=db.backref("resources", lazy=True))
    cluster = db.relationship("Cluster", backref=db.backref("resources", lazy=True))

class YamlEdit(db.Model):
    __tablename__ = "yaml_edits"

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id", ondelete="CASCADE"))
    edited_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    old_yaml = db.Column(db.Text)
    new_yaml = db.Column(db.Text)
    applied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resource = db.relationship("Resource", backref=db.backref("yaml_edits", lazy=True))
    editor = db.relationship("User", backref=db.backref("yaml_edits", lazy=True))

class MetricsCache(db.Model):
    __tablename__ = "metrics_cache"

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id", ondelete="CASCADE"))
    metric_name = db.Column(db.String(255), nullable=False)
    metric_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    resource = db.relationship("Resource", backref=db.backref("metrics_cache", lazy=True))

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("audit_logs", lazy=True))

class DashboardSetting(db.Model):
    __tablename__ = "dashboard_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    layout = db.Column(db.JSON)
    filters = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("dashboard_settings", lazy=True))
