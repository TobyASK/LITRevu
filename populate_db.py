"""
Script pour générer des données de test pour l'application LITRevu.
"""
import os
import django
from django.contrib.auth import get_user_model
from reviews.models import Ticket, Review, UserFollows

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litrevu.settings')
django.setup()

User = get_user_model()


def create_users():
    """Créer des utilisateurs de test."""
    users_data = [
        {'username': 'admin', 'password': 'admin123', 'is_superuser': True,
         'is_staff': True, 'email': 'admin@litrevu.com'},
        {'username': 'alice', 'password': 'alice123',
         'email': 'alice@email.com'},
        {'username': 'bob', 'password': 'bob123', 'email': 'bob@email.com'},
        {'username': 'charlie', 'password': 'charlie123',
         'email': 'charlie@email.com'},
        {'username': 'diane', 'password': 'diane123',
         'email': 'diane@email.com'},
    ]

    users = {}
    for data in users_data:
        is_superuser = data.pop('is_superuser', False)
        is_staff = data.pop('is_staff', False)
        password = data.pop('password')

        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={'email': data.get('email', ''),
                      'is_superuser': is_superuser, 'is_staff': is_staff}
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"Utilisateur créé: {user.username}")
        else:
            print(f"Utilisateur existant: {user.username}")

        users[data['username']] = user

    return users


def create_follows(users):
    """Créer des relations de suivi entre utilisateurs."""
    follows = [
        ('alice', 'bob'),
        ('alice', 'charlie'),
        ('bob', 'alice'),
        ('bob', 'diane'),
        ('charlie', 'alice'),
        ('charlie', 'bob'),
        ('diane', 'alice'),
    ]

    for follower, followed in follows:
        _, created = UserFollows.objects.get_or_create(
            user=users[follower],
            followed_user=users[followed]
        )
        if created:
            print(f"{follower} suit maintenant {followed}")


def create_tickets(users):
    """Créer des billets de test."""
    tickets_data = [
        {
            'user': 'alice',
            'title': 'Le Petit Prince',
            'description': "Recherche avis sur ce classique d'Antoine de "
                           "Saint-Exupéry. L'avez-vous lu ? Qu'en "
                           "pensez-vous ?"
        },
        {
            'user': 'bob',
            'title': '1984 - George Orwell',
            'description': 'Un roman dystopique incontournable. Je cherche '
                           'des critiques détaillées sur cette œuvre.'
        },
        {
            'user': 'charlie',
            'title': 'Clean Code - Robert C. Martin',
            'description': 'Livre technique sur les bonnes pratiques de '
                           'développement. Recommandé pour les développeurs ?'
        },
        {
            'user': 'alice',
            'title': "L'Étranger - Albert Camus",
            'description': "Chef-d'œuvre de la littérature française. "
                           "J'aimerais avoir vos impressions."
        },
        {
            'user': 'diane',
            'title': 'Harry Potter à l\'école des sorciers',
            'description': 'Premier tome de la saga. Adapté pour quel âge ?'
        },
    ]

    tickets = {}
    for data in tickets_data:
        ticket, created = Ticket.objects.get_or_create(
            user=users[data['user']],
            title=data['title'],
            defaults={'description': data['description']}
        )
        if created:
            print(f"Billet créé: {ticket.title}")
        tickets[data['title']] = ticket

    return tickets


def create_reviews(users, tickets):
    """Créer des critiques de test."""
    reviews_data = [
        {
            'user': 'bob',
            'ticket_title': 'Le Petit Prince',
            'headline': 'Un conte philosophique magnifique',
            'rating': 5,
            'body': "Ce livre m'a profondément touché. Une lecture "
                    "essentielle qui nous rappelle l'importance de voir avec "
                    "le cœur. L'écriture est poétique et accessible à tous."
        },
        {
            'user': 'charlie',
            'ticket_title': '1984 - George Orwell',
            'headline': 'Plus actuel que jamais',
            'rating': 5,
            'body': "Une œuvre visionnaire qui résonne particulièrement "
                    "aujourd'hui. La description de Big Brother est glaçante. "
                    "À lire absolument."
        },
        {
            'user': 'alice',
            'ticket_title': 'Clean Code - Robert C. Martin',
            'headline': 'Indispensable pour tout développeur',
            'rating': 4,
            'body': "Des conseils pratiques et pertinents pour écrire du code "
                    "propre. Quelques exemples un peu datés mais les "
                    "principes restent valables."
        },
        {
            'user': 'diane',
            'ticket_title': 'Le Petit Prince',
            'headline': 'Poétique mais simple',
            'rating': 4,
            'body': "Une belle histoire, mais je m'attendais à quelque chose "
                    "de plus profond. Reste une lecture agréable."
        },
    ]

    for data in reviews_data:
        ticket = tickets.get(data['ticket_title'])
        if ticket:
            review, created = Review.objects.get_or_create(
                user=users[data['user']],
                ticket=ticket,
                defaults={
                    'headline': data['headline'],
                    'rating': data['rating'],
                    'body': data['body']
                }
            )
            if created:
                print(f"Critique créée: {review.headline}")


def main():
    """Fonction principale."""
    print("=" * 50)
    print("Création des données de test pour LITRevu")
    print("=" * 50)

    print("\n--- Création des utilisateurs ---")
    users = create_users()

    print("\n--- Création des abonnements ---")
    create_follows(users)

    print("\n--- Création des billets ---")
    tickets = create_tickets(users)

    print("\n--- Création des critiques ---")
    create_reviews(users, tickets)

    print("\n" + "=" * 50)
    print("Données de test créées avec succès !")
    print("=" * 50)
    print("\nComptes utilisateurs disponibles:")
    print("-" * 30)
    print("Admin:    admin / admin123")
    print("Alice:    alice / alice123")
    print("Bob:      bob / bob123")
    print("Charlie:  charlie / charlie123")
    print("Diane:    diane / diane123")
    print("-" * 30)


if __name__ == '__main__':
    main()
